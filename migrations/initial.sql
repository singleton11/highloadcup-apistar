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
  ON users (id);

CREATE TABLE locations
(
  id       INT PRIMARY KEY NOT NULL,
  place    TEXT            NOT NULL,
  country  VARCHAR(50)     NOT NULL,
  city     VARCHAR(50)     NOT NULL,
  distance INT             NOT NULL
);
CREATE UNIQUE INDEX locations_id_uindex
  ON locations (id);

CREATE TABLE visits
(
  id         INT PRIMARY KEY NOT NULL,
  location   INT             NOT NULL,
  user       INT             NOT NULL,
  visited_at INT             NOT NULL,
  mark       INT(1),
  CONSTRAINT visits_locations_id_fk FOREIGN KEY (location) REFERENCES locations (id),
  CONSTRAINT visits_users_id_fk FOREIGN KEY (user) REFERENCES users (id)
);
CREATE UNIQUE INDEX visits_id_uindex
  ON visits (id);