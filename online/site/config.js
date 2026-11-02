/* My Travel Map Online — connection settings.
   Fill in the two values from Supabase → Project Settings → API (or "Connect" → App Frameworks):
     supabaseUrl      = Project URL, e.g. https://abcdefghijklmnop.supabase.co
     supabaseAnonKey  = the "anon" / "publishable" public key (NOT the service_role / secret key)
   Both values are safe to publish: every person's data is protected by Row Level Security. */
window.TRAVEL_MAP_CONFIG = {
  supabaseUrl: "YOUR_SUPABASE_PROJECT_URL",
  supabaseAnonKey: "YOUR_SUPABASE_ANON_KEY"
};
