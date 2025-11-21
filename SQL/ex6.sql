-- EX6.SQL — Data Modification Commands
-- Three non-trivial data modification statements.
SET SQL_SAFE_UPDATES = 0;
USE WildlifeTravelDB;

-- ============================================================
-- 1. UPDATE:
-- Increase helpfulCount for users who travelled to Kenya.
-- ============================================================
UPDATE Review
SET helpfulCount = helpfulCount + 5
WHERE userEmail IN (
    SELECT userEmail
    FROM Trip
    WHERE destination = 'Kenya'
);

-- ============================================================
-- 2. DELETE:
-- Remove sightings of "Least Concern" species before July 2024.
-- ============================================================
DELETE FROM Sighting
WHERE observedAt < '2024-07-01'
  AND speciesID IN (
        SELECT speciesID
        FROM Species
        WHERE conservationStatus = 'Least Concern'
  );

-- ============================================================
-- 3. INSERT ... SELECT:
-- Create reviews automatically for Canadian users at Lake Louise,
-- but only if they do not already have a review there.
-- (Uses ROW_NUMBER() window function — requires MySQL 8+.)
-- ============================================================
INSERT INTO Review (
    reviewID, userEmail, locationID, rating,
    reviewText, datePosted, helpfulCount
)
SELECT 
    (800 + ROW_NUMBER() OVER (ORDER BY u.userEmail)) AS reviewID,
    u.userEmail,
    403 AS locationID,  -- Lake Louise
    5   AS rating,
    CONCAT('Auto-generated review for ', u.firstName,
           ': Loved Lake Louise!') AS reviewText,
    CURDATE() AS datePosted,
    0 AS helpfulCount
FROM User u
WHERE u.country = 'Canada'
  AND u.userEmail NOT IN (
        SELECT userEmail
        FROM Review
        WHERE locationID = 403
  );
