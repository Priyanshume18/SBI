import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://nioaahptydompdsysqbl.supabase.co'; // replace with your actual Supabase project URL
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5pb2FhaHB0eWRvbXBkc3lzcWJsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM4ODA5ODgsImV4cCI6MjA2OTQ1Njk4OH0.o4lJz7cUc18dA3Ozy59wESdiZ9zC3Lp-4e6T7GfVNIg'; // replace with your anon/public key

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
