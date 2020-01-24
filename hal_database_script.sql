CREATE TABLE "Category" (
	"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Type"	TEXT NOT NULL
)

CREATE TABLE "Company" (
	"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Name"	TEXT NOT NULL,
	"Country"	TEXT NOT NULL,
	"CategoryID"	INTEGER NOT NULL,
	"EmployeeCount"	INTEGER NOT NULL,
	FOREIGN KEY("CategoryID") REFERENCES "Category"("ID")
)

CREATE TABLE "Event" (
	"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Date"	INTEGER NOT NULL,
	"CompanyID"	INTEGER NOT NULL,
	"Type"	TEXT NOT NULL,
	FOREIGN KEY("CompanyID") REFERENCES "Company"("ID")
)

CREATE TABLE "Links" (
	"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"ParentID"	INTEGER NOT NULL,
	"ChildID"	INTEGER NOT NULL,
	"Percent"	INTEGER NOT NULL,
	FOREIGN KEY("ParentID") REFERENCES "Company"("ID"),
	FOREIGN KEY("ChildID") REFERENCES "Company"("ID")
)

CREATE TABLE "OperationCountry" (
	"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"CompanyID"	INTEGER NOT NULL,
	"Country"	TEXT NOT NULL,
	"Date"	INTEGER NOT NULL,
	FOREIGN KEY("CompanyID") REFERENCES "Company"("ID")
)

CREATE TABLE "Sale" (
	"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Date"	INTEGER NOT NULL,
	"Value"	REAL NOT NULL,
	"CompanyID"	INTEGER NOT NULL,
	FOREIGN KEY("CompanyID") REFERENCES "Company"("ID")
)

CREATE TABLE "Stock" (
	"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Date"	INTEGER NOT NULL,
	"Value"	REAL NOT NULL,
	"CompanyID"	INTEGER NOT NULL,
	FOREIGN KEY("CompanyID") REFERENCES "Company"("ID")
)

INSERT INTO Category VALUES(1, 'electronic');
INSERT INTO Category VALUES(2, 'shipping');
INSERT INTO Category VALUES(3, 'food');
INSERT INTO Category VALUES(4, 'commerce');
INSERT INTO Category VALUES(5, 'airplane manufacturers');

INSERT INTO Company VALUES(1, 'sony', 'japan', 1, 114400);
INSERT INTO Company VALUES(2, 'amazon', 'usa', 4, 647500);
INSERT INTO Company VALUES(3, 'airbus', 'netherlands', 5, 133671);

INSERT INTO OperationCountry VALUES(1, 1, 'belgium', 2019);
INSERT INTO OperationCountry VALUES(2, 1, 'usa', 2019);
INSERT INTO OperationCountry VALUES(3, 1, 'england', 2019);
INSERT INTO OperationCountry VALUES(4, 1, 'japan', 2019);
INSERT INTO OperationCountry VALUES(5, 1, 'china', 2019);

INSERT INTO OperationCountry VALUES(6, 2, 'belgium', 2019);
INSERT INTO OperationCountry VALUES(7, 2, 'usa', 2019);
INSERT INTO OperationCountry VALUES(8, 2, 'england', 2019);
INSERT INTO OperationCountry VALUES(9, 2, 'netherlands', 2019);
INSERT INTO OperationCountry VALUES(10, 2, 'spain', 2019);

INSERT INTO OperationCountry VALUES(11, 3, 'france', 2019);
INSERT INTO OperationCountry VALUES(12, 3, 'congo', 2019);
INSERT INTO OperationCountry VALUES(13, 3, 'poland', 2019);
INSERT INTO OperationCountry VALUES(14, 3, 'usa', 2019);
INSERT INTO OperationCountry VALUES(15, 3, 'netherlands', 2019);

INSERT INTO Sale Values(1, 2019, 9000000, 1);
INSERT INTO Sale Values(2, 2019, 25000000, 2);
INSERT INTO Sale Values(3, 2019, 14000000, 3);

INSERT INTO Stock Values(1, 2019, 1.5, 1);
INSERT INTO Stock Values(2, 2019, 2, 2);
INSERT INTO Stock Values(3, 2019, 1.02, 3);

INSERT INTO Event Values(1, 1946, 1, 'founded');
INSERT INTO Event Values(2, 1994, 2, 'founded');
INSERT INTO Event Values(3, 1970, 3, 'founded');

INSERT INTO Links Values(1, 1, 2, 15);
INSERT INTO Links Values(2, 2, 3, 51);
INSERT INTO Links Values(3, 1, 3, 48);

INSERT INTO Category VALUES(6, 'chocolatier');
INSERT INTO Category VALUES(7, 'car manufacturer');
INSERT INTO Category VALUES(8, 'transport');
INSERT INTO Company VALUES(4, 'google', 'china', 1, 123456);
INSERT INTO Company VALUES(5, 'tao', 'france', 3, 147852);
INSERT INTO Company VALUES(6, 'coca', 'usa', 3, 213547);
INSERT INTO Company VALUES(7, 'moodys', 'usa', 1, 50123);
INSERT INTO Company VALUES(8, 'dell', 'england', 1, 12001);
INSERT INTO Company VALUES(9, 'msi', 'usa', 1, 13251);
INSERT INTO Company VALUES(10, 'okta', 'usa', 1, 10549);
INSERT INTO Company VALUES(11, 'mcdo', 'usa', 3, 5412);
INSERT INTO Company VALUES(12, 'dakine', 'netherlands', 4, 6421);
INSERT INTO Company VALUES(13, 'cisco', 'usa', 1, 12254);
INSERT INTO Company VALUES(14, 'samsung', 'china', 1, 154264);
INSERT INTO Company VALUES(15, 'zara', 'spain', 4, 5214);
INSERT INTO Company VALUES(16, 'alcatel', 'france', 1, 12350);
INSERT INTO Company VALUES(17, 'philips', 'netherlands', 1, 52143);
INSERT INTO Company VALUES(18, 'spa', 'belgium', 3, 5213);
INSERT INTO Company VALUES(19, 'tesla', 'usa', 7, 164258);
INSERT INTO Company VALUES(20, 'ford', 'usa', 7, 154789);
INSERT INTO Company VALUES(21, 'toyota', 'japan', 7, 145632);
INSERT INTO Company VALUES(22, 'bmw', 'germany', 7, 159847);
INSERT INTO Company VALUES(23, 'stib', 'belgium', 8, 12458);
INSERT INTO Company VALUES(24, 'valrhoma', 'france', 6, 4215);

INSERT INTO Event Values(4, 1998, 4, 'founded');
INSERT INTO Event Values(5, 1995, 5, 'founded');
INSERT INTO Event Values(6, 1964, 6, 'founded');
INSERT INTO Event Values(7, 1909, 7, 'founded');
INSERT INTO Event Values(8, 1965, 8, 'founded');
INSERT INTO Event Values(9, 2001, 9, 'founded');
INSERT INTO Event Values(10, 2009, 10, 'founded');
INSERT INTO Event Values(11, 1970, 11, 'founded');
INSERT INTO Event Values(12, 2005, 12, 'founded');
INSERT INTO Event Values(13, 1970, 13, 'founded');
INSERT INTO Event Values(14, 1984, 14, 'founded');
INSERT INTO Event Values(15, 2003, 15, 'founded');
INSERT INTO Event Values(16, 1997, 16, 'founded');
INSERT INTO Event Values(17, 1970, 17, 'founded');
INSERT INTO Event Values(18, 1984, 18, 'founded');
INSERT INTO Event Values(19, 2001, 19, 'founded');
INSERT INTO Event Values(20, 1946, 20, 'founded');
INSERT INTO Event Values(21, 1998, 21, 'founded');
INSERT INTO Event Values(22, 1970, 22, 'founded');
INSERT INTO Event Values(23, 1970, 23, 'founded');
INSERT INTO Event Values(24, 2001, 24, 'founded');

INSERT INTO Stock Values(4, 2018, 1.15, 3);
INSERT INTO Stock Values(5, 2017, 1.08, 3);
INSERT INTO Stock Values(6, 2016, 1.21, 3);
INSERT INTO Stock Values(7, 2015, 0.95, 3);
INSERT INTO Stock Values(8, 2014, 0.91, 3);

INSERT INTO Links Values(5, 4, 1, 2);
INSERT INTO Links Values(6, 5, 1, 6);
INSERT INTO Links Values(7, 6, 1, 7);
INSERT INTO Links Values(8, 7, 1, 24);
INSERT INTO Links Values(9, 8, 1, 1);
INSERT INTO Links Values(10, 9, 1, 1);
INSERT INTO Links Values(11, 10, 1, 2);
INSERT INTO Links Values(12, 11, 1, 8);
INSERT INTO Links Values(13, 12, 1, 4);
INSERT INTO Links Values(14, 13, 1, 4);

INSERT INTO Links Values(15, 14, 3, 1);
INSERT INTO Links Values(16, 15, 3, 2);
INSERT INTO Links Values(17, 16, 3, 1);
INSERT INTO Links Values(18, 17, 3, 14);
INSERT INTO Links Values(19, 18, 3, 12);
INSERT INTO Links Values(20, 19, 3, 7);
INSERT INTO Links Values(21, 20, 3, 5);
INSERT INTO Links Values(22, 21, 3, 5);
INSERT INTO Links Values(23, 22, 3, 3);
INSERT INTO Links Values(24, 23, 3, 3);
INSERT INTO Links Values(25, 24, 3, 1);