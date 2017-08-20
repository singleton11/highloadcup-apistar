CREATE TABLE users
(
  id         INT PRIMARY KEY NOT NULL,
  email      VARCHAR(100)    NOT NULL,
  first_name VARCHAR(50)     NOT NULL,
  last_name  VARCHAR(50)     NOT NULL,
  gender     BOOLEAN DEFAULT TRUE NOT NULL,
  birth_date INT             NOT NULL
);
CREATE UNIQUE INDEX users_email_uindex
  ON users (email);
CREATE UNIQUE INDEX users_id_uindex
  ON users (id)