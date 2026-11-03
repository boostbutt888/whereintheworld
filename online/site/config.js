/* My Travel Map Online — connection settings.
   Values from Supabase → Project Settings → API Keys (or "Connect" → App Frameworks):
     supabaseUrl      = Project URL
     supabaseAnonKey  = the whole "publishable" key, starting "sb_publishable_" (NOT the secret / service_role key)
   Both values are safe to publish: every person's data is protected by Row Level Security. */
window.TRAVEL_MAP_CONFIG = {
  supabaseUrl: "https://vonjvfthupuarxhhtahh.supabase.co",
  supabaseAnonKey: "sb_publishable_M4i3XU91P5bKdcgUwGEX7w_vmkH5OGn"
};
