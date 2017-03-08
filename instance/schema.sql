CREATE TABLE IF NOT EXISTS user (
  fullname text PRIMARY KEY,
  city text NOT NULL,
  state text NOT NULL,
  email text(254) NOT NULL,
  verify_token text NOT NULL,
  submitted_on integer NOT NULL,
  verified_on integer
);
