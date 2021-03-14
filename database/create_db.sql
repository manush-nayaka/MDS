PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE packages(id CHARACTER(20) PRIMARY KEY, created_dt TIMESTAMP DEFAUlT CURRENT_TIMESTAMP NOT NULL, destination_address VARCHAR NOT NULL, destination_city VARCHAR NOT NULL, delivered BOOLEAN DEFAULT 0);
CREATE TABLE transits(transit_id CHARACTER(20) primary key not null, package_id CHARACTER(20) not null, transit_address VARCHAR NOT NULL, timestamp DEFAUlT CURRENT_TIMESTAMP NOT NULL, CONSTRAINT fk_package_id foreign key (package_id) references packages(id));
COMMIT;
