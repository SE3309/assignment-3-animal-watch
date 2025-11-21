-- EX5.SQL — SELECT Queries for Assignment 3
-- Contains seven SELECT–FROM–WHERE queries.
-- Six use advanced SQL features; one is intentionally simple.

USE WildlifeTravelDB;

-- ============================================================
-- Query 1 (Simple Query)
-- List all trips starting after July 1, 2024.
-- ============================================================
SELECT tripID, tripName, destination, startDate
FROM Trip
WHERE startDate > '2024-07-01';

-- ============================================================
-- Query 2 (JOIN Across 3 Tables)
-- Show sightings with species name, location name, and user.
-- ============================================================
SELECT S.sightingID,
       Sp.commonName AS species,
       L.name        AS location,
       S.userEmail,
       S.observedAt
FROM Sighting S
JOIN Species  Sp ON S.speciesID  = Sp.speciesID
JOIN Location L  ON S.locationID = L.locationID
WHERE S.observedAt IS NOT NULL;

-- ============================================================
-- Query 3 (Subquery using IN)
-- List users who have written at least one review.
-- ============================================================
SELECT userEmail, firstName, lastName
FROM User
WHERE userEmail IN (
    SELECT userEmail
    FROM Review
);

-- ============================================================
-- Query 4 (EXISTS)
-- Show locations that have at least one recorded sighting.
-- ============================================================
SELECT L.locationID, L.name, L.region
FROM Location L
WHERE EXISTS (
    SELECT 1
    FROM Sighting S
    WHERE S.locationID = L.locationID
);

-- ============================================================
-- Query 5 (GROUP BY + HAVING)
-- Count reviews per location; show only those with > 1 review.
-- ============================================================
SELECT L.locationID,
       L.name,
       COUNT(R.reviewID) AS reviewCount
FROM Location L
JOIN Review R ON L.locationID = R.locationID
GROUP BY L.locationID, L.name
HAVING COUNT(R.reviewID) > 1;

-- ============================================================
-- Query 6 (Nested Subqueries + Aggregation)
-- Show species with more sightings than the average species.
-- ============================================================
SELECT Sp.speciesID,
       Sp.commonName
FROM Species Sp
WHERE (
    SELECT COUNT(*)
    FROM Sighting S
    WHERE S.speciesID = Sp.speciesID
) >
(
    SELECT AVG(specCount)
    FROM (
        SELECT speciesID, COUNT(*) AS specCount
        FROM Sighting
        GROUP BY speciesID
    ) AS counts
);

-- ============================================================
-- Query 7 (JOIN + GROUP BY)
-- Show each user and the number of corporate-backed trips
-- they took.
-- ============================================================
SELECT U.userEmail,
       U.firstName,
       U.lastName,
       COUNT(T.tripID) AS totalTrips
FROM User U
JOIN Trip T ON U.userEmail = T.userEmail
WHERE T.cAccountID IS NOT NULL
GROUP BY U.userEmail, U.firstName, U.lastName;
