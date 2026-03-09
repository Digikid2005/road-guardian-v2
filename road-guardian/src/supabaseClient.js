import { createClient } from "@supabase/supabase-js";

const SUPABASE_URL = "https://vxxenzygxzkejqqronbv.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ4eGVuenlneHprZWpxcXJvbmJ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ0MTQ1ODIsImV4cCI6MjA3OTk5MDU4Mn0.xOYm_17guTBNcRzEpTXkGnB1X-RdpX_g5NmGFiAlU2s"; 

export const supabase = createClient(
  SUPABASE_URL,
  SUPABASE_ANON_KEY
);
