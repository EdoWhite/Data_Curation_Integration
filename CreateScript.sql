CREATE TABLE "event" (
  "id" varchar(100) PRIMARY KEY,
  "date_start_id" int,
  "date_end_id" int,
  "location_id" int,
  "source" varchar(200),
  "shortname" varchar(200),
  "title" varchar(200)
);

CREATE TABLE "date" (
  "id" int PRIMARY KEY,
  "day" int,
  "month" int,
  "year" int
);

CREATE TABLE "accomodation" (
  "id" varchar(100) PRIMARY KEY,
  "location_id" int,
  "source" varchar(30),
  "has_room" boolean,
  "acco_type_id" varchar(50),
  "shortname" varchar(100),
  "is_bookable" boolean,
  "name" varchar(100),
  "website" varchar(400),
  "lang" varchar(10),
  "phone" varchar(20)
);

CREATE TABLE "location" (
  "id" int PRIMARY KEY,
  "zip" int,
  "city" varchar(100),
  "latitude" float,
  "longitude" float,
  "street" varchar(100),
  "country_code" varchar(20)
);

CREATE TABLE "parkplace" (
  "id" varchar(100) PRIMARY KEY,
  "location_id" int,
  "name" varchar(100),
  "available" boolean,
  "active" boolean,
  "origin" varchar(100),
  "type" varchar(100)
);

ALTER TABLE "event" ADD FOREIGN KEY ("date_start_id") REFERENCES "date" ("id");

ALTER TABLE "event" ADD FOREIGN KEY ("date_end_id") REFERENCES "date" ("id");

ALTER TABLE "event" ADD FOREIGN KEY ("location_id") REFERENCES "location" ("id");

ALTER TABLE "accomodation" ADD FOREIGN KEY ("location_id") REFERENCES "location" ("id");

ALTER TABLE "parkplace" ADD FOREIGN KEY ("location_id") REFERENCES "location" ("id");
