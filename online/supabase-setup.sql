-- My Travel Map Online — Supabase database setup
-- Paste this whole file into Supabase → SQL Editor → New query → Run.
-- Safe to run more than once.

-- One row per signed-in person. "data" holds exactly the same JSON
-- structure as the desktop app's travel-data.json (profile + places).
create table if not exists public.travel_maps (
  user_id    uuid primary key references auth.users(id) on delete cascade default auth.uid(),
  data       jsonb  not null default '{}'::jsonb,
  revision   bigint not null default 0,
  updated_at timestamptz not null default now(),
  -- keep any single person's database to a sane size (about 5 MB ≈ 20,000+ places)
  constraint travel_maps_size check (pg_column_size(data) < 5000000)
);

-- Row Level Security: a person can only ever see or change their own row.
alter table public.travel_maps enable row level security;

drop policy if exists "own row: read"   on public.travel_maps;
drop policy if exists "own row: insert" on public.travel_maps;
drop policy if exists "own row: update" on public.travel_maps;
drop policy if exists "own row: delete" on public.travel_maps;

create policy "own row: read"   on public.travel_maps for select to authenticated using (user_id = (select auth.uid()));
create policy "own row: insert" on public.travel_maps for insert to authenticated with check (user_id = (select auth.uid()));
create policy "own row: update" on public.travel_maps for update to authenticated using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));
create policy "own row: delete" on public.travel_maps for delete to authenticated using (user_id = (select auth.uid()));

revoke all on public.travel_maps from anon;
grant select, insert, update, delete on public.travel_maps to authenticated;

-- Safe save: only succeeds if nobody else (another tab / device) saved since
-- this browser last loaded. Same protection as the desktop app's 409 "stale".
-- Returns the new revision number.
create or replace function public.save_travel_map(p_data jsonb, p_base_revision bigint)
returns bigint
language plpgsql
security invoker
set search_path = public
as $$
declare
  uid uuid := auth.uid();
  new_rev bigint;
begin
  if uid is null then
    raise exception 'not signed in' using errcode = '28000';
  end if;
  if p_data is null or jsonb_typeof(p_data) <> 'object'
     or coalesce(jsonb_typeof(p_data->'places'), '') <> 'array' then
    raise exception 'invalid travel data' using errcode = '22023';
  end if;

  update public.travel_maps
     set data = p_data, revision = revision + 1, updated_at = now()
   where user_id = uid and revision = coalesce(p_base_revision, 0)
  returning revision into new_rev;

  if new_rev is null then
    if exists (select 1 from public.travel_maps where user_id = uid) then
      raise exception 'stale: your travel map was changed in another tab or device — reload the page' using errcode = '40001';
    end if;
    if coalesce(p_base_revision, 0) <> 0 then
      raise exception 'stale: your travel map is missing on the server — reload the page' using errcode = '40001';
    end if;
    insert into public.travel_maps (user_id, data, revision) values (uid, p_data, 1)
    returning revision into new_rev;
  end if;
  return new_rev;
end;
$$;

revoke all on function public.save_travel_map(jsonb, bigint) from public, anon;
grant execute on function public.save_travel_map(jsonb, bigint) to authenticated;
