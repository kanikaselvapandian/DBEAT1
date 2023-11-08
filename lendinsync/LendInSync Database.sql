-- This .sql file performs a complete refresh of all database information.

-- System settings
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;

-- --------------------------------------------------------
-- WALLET

-- Create database
CREATE DATABASE IF NOT EXISTS `lis_wallet`
DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `lis_wallet`;

-- Table structure for table `wallet`
DROP TABLE IF EXISTS `Wallet`;
CREATE TABLE IF NOT EXISTS `Wallet` 
(
    `WID` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `CustomerId` VARCHAR(512),
    `CurrencyCode` VARCHAR(512),
    `Amount` DECIMAL(18, 2)
) ENGINE = InnoDB DEFAULT CHARSET=utf8;

-- Insert values for Wallet table
INSERT INTO `Wallet` (WID, CustomerId, CurrencyCode, Amount) VALUES
('1', 'A123456', 'VND', '2725451'),
('2', 'A123456', 'USD', '97.61'),
('3', 'A123456', 'AUD', '174.943'),
('4', 'A123456', 'BBD', '202.955'),
('5', 'A123456', 'JPY', '25723.80'),
('6', 'S9934651E', 'NZD', '298.138'),
('7', 'S9934651E', 'USD', '173.753'),
('8', 'S9934651E', 'AED', '710.489'),
('9', 'S9934651E', 'CHF', '173.132'),
('10', 'S9934651E', 'KYD', '182.513'),
('11', 'H123123', 'CAD', '301.572'),
('12', 'H123123', 'BND', '312'),
('13', 'H123123', 'CNY', '1601.89'),
('14', 'H123123', 'ISK', '27884.70'),
('15', 'H123123', 'INR', '16688.40'),
('16', 'H123123', 'USD', '154.89'),
('17', 'S9934651E', 'JPY', '27037.40'),
('18', 'A123456', 'KWD', '33.7801'),
('19', 'S9934651E', 'MYR', '523.182'),
('20', 'H123123', 'NZD', '202.934');
COMMIT;

-- --------------------------------------------------------
-- WALLET TRANSACTION

-- Create database
CREATE DATABASE IF NOT EXISTS `lis_transaction`
DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `lis_transaction`;

-- Table structure for table `WalletTransaction`
DROP TABLE IF EXISTS `WalletTransaction`;
CREATE TABLE IF NOT EXISTS `WalletTransaction` 
(
    `TID` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `SourceWallet` INT,
    `DestinationWallet` INT,
    `CustomerId` VARCHAR(512) NOT NULL,
    `AmountTransferred` DECIMAL(18, 2),
    `WalletTransaction` BOOLEAN,
    `ExchangeRate` DECIMAL(18, 5),
    `TimeStamp` TIMESTAMP
) ENGINE = InnoDB DEFAULT CHARSET=utf8;

-- Insert values for WalletTransaction table
INSERT INTO `WalletTransaction` (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES
('1', '1', '4', 'A123456', '50000', TRUE, '0.00008', '2023-07-07 10:39:38'),
('2', '3', '5', 'A123456', '50', TRUE, '95.0925', '2023-07-06 09:39:45'),
('3', '5', '2', 'A123456', '10000', TRUE, '0.00667', '2023-07-03 11:15:31'),
('4', '4', '5', 'A123456', '150.85', TRUE, '74.969', '2023-07-01 12:19:25'),
('5', '2', '5', 'A123456', '75', TRUE, '149.938', '2023-08-28 10:18:01'),
('6', '4', '1', 'A123456', '120', TRUE, '12280.40', '2023-08-15 09:45:43'),
('7', '1', NULL, 'H123123', '1200000', FALSE, '0.00006', '2023-08-10 13:39:52'),
('8', '2', NULL, 'H123123', '20', FALSE, '1.36957', '2023-08-06 22:27:12'),
('9', NULL, '4', 'H123123', '50', FALSE, '1.46011', '2023-08-29 21:28:31'),
('10', NULL, '5', 'H123123', '45', FALSE, '109.463', '2023-09-22 19:47:13'),
('11', '6', '7', 'H123123', '123.5', TRUE, '0.58264', '2023-09-18 18:39:37'),
('12', '7', '8', 'H123123', '85.7', TRUE, '3.67246', '2023-09-04 15:27:29'),
('13', '8', '9', 'S9934651E', '350.6', TRUE, '0.24361', '2023-09-27 05:06:35'),
('14', '9', '10', 'S9934651E', '56.8', TRUE, '0.93102', '2023-09-17 07:19:37'),
('15', '7', NULL, 'S9934651E', '65', FALSE, '1.36957', '2023-10-07 10:28:29'),
('16', '9', NULL, 'S9934651E', '100.45', FALSE, '1.53011', '2023-10-01 10:31:18'),
('17', NULL, '6', 'S9934651E', '67', FALSE, '1.25268', '2023-10-23 09:42:16'),
('18', NULL, '9', 'S9934651E', '30', FALSE, '0.65333', '2023-11-06 14:39:18'),
('19', NULL, '10', 'S9934651E', '105', FALSE, '0.60838', '2023-11-07 17:28:17');
COMMIT;

-- --------------------------------------------------------
-- LOANS

-- Create database
CREATE DATABASE IF NOT EXISTS `lis_loan`
DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `lis_loan`;

-- Table structure for table `Loan`
DROP TABLE IF EXISTS `Loan`;
CREATE TABLE IF NOT EXISTS `Loan` 
(
    `LoanId` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `CustomerId` VARCHAR(512),
    `OtherPartyId` VARCHAR(512),
    `CollateralAmount` DECIMAL(18, 2),
    `LoanAmount` DECIMAL(18, 2),
    `InvestmentAmount` DECIMAL(18, 2),
    `InterestRate` DECIMAL(5, 2),
    `CurrencyCode` VARCHAR(512),
    `TotalInterestAmount` INT,
    `ServiceFee` DECIMAL(18, 2),
    `RepaymentAmount` DECIMAL(18, 2),
    `Revenue` DECIMAL(18, 2),
    `LoanTerm` INT,
    `StartDate` TIMESTAMP,
    `EndDate` TIMESTAMP,
    `StatusLevel` VARCHAR(512)
) ENGINE = InnoDB DEFAULT CHARSET=utf8;

-- Insert values for Loan table
INSERT INTO `Loan` (LoanId, CustomerId, OtherPartyId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode, TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel)
VALUES
('1', 'A123456', 'S9934651E','1000', '800', '800', '10', 'USD', '80', '8', '880', '880', '365', '2023-10-15 10:39:37', '2024-10-14 10:39:37', 'BMatch'),
('2', 'S9934651E', 'H123123', '1000', '800', '800', '10', 'USD', '80', '8', '880', '880', '365', '2022-12-27 09:39:37', '2023-12-27 09:39:37', 'LMatch'),
('3', 'H123123', NULL,'500', '400', NULL, NULL, 'NZD', NULL, '4', NULL, NULL, '365', NULL, NULL, 'Borrowing'),
('4', 'A123456', 'H123123','1500', '1200','1200', '12', 'USD', '144', '12', '1344', '1344', '365', '2022-08-10 10:39:37', '2023-08-10 10:39:37', 'Closed'),
('5', 'A123456', NULL, NULL, '1000', '1000', '10', 'AED', '50', '10', '1050', '1050', '180', NULL, NULL, 'Lending'),
('6', 'A123456', 'H123123', '7500', '5000', '5000', '10', 'CHF', '500', '50', '5500', '5500', '365', '2022-09-07 10:39:37', '2023-09-07 10:39:37', 'Closed'),
('7', 'A123456', NULL,'10000', '7000', '7000', NULL, 'KYD', '700', '70', '7750', NULL, '365', NULL, NULL, 'Borrowing'),
('8', 'A123456', NULL,'10000', '7000', '7000', NULL, 'USD', '700', '70', '7750', NULL, '365', NULL, NULL, 'Borrowing'),
('9', 'A123456', 'S9934651E', '3000', '2000', '2000', '10', 'USD', '100', '20', '2100', '2100', '180', '2023-08-12 10:39:37', '2024-02-08 10:39:37', 'BMatch'),
('10', 'S9934651E', NULL,NULL, NULL, '5000', '10', 'AUD', '500', '50', '5500', '5500', '365', NULL, NULL, 'Lending'),
('11', 'S9934651E', NULL,NULL, NULL, '10000', '10', 'BBD', '1000', '100', '11000', '11000', '365', NULL, NULL, 'Lending'),
('12', 'S9934651E', NULL, NULL, '1000', '1000', '10', 'USD', '50', '10', '1050', '1050', '180', NULL, NULL, 'Lending'),
('13', 'S9934651E', NULL,'10000', '7000', '7000', NULL, 'KYD', '700', '70', '7750', NULL, '365', NULL, NULL, 'Borrowing'),
('14', 'H123123', NULL,'10000', '7000', '7000', NULL, 'KYD', '700', '70', '7750', NULL, '365', NULL, NULL, 'Borrowing'),
('15', 'S9934651E',  NULL, NULL, '1000', '1000', '10', 'JPY', '50', '10', '1050', '1050', '180', NULL, NULL, 'Lending'),
('16', 'H123123', 'S9934651E', '1000', '800', '800', '10', 'USD', '80', '8', '880', '880', '365', '2022-12-27 09:39:37', '2023-12-27 09:39:37', 'LMatch'),
('17', 'H123123', 'A123456', '1000', '800', '800', '10', 'USD', '80', '8', '880', '880', '365', '2022-12-27 09:39:37', '2023-12-27 09:39:37', 'LMatch'),
('18', 'H123123',  NULL, NULL, '1000', '1000', '10', 'AED', '50', '10', '1050', '1050', '180', NULL, NULL, 'Lending'),
('19', 'A123456', 'S9934651E','1000', '800', '800', '10', 'USD', '80', '8', '880', '880', '365', '2023-10-15 10:39:37', '2024-10-14 10:39:37', 'BMatch'),
('20', 'H123123',  NULL, NULL, '1000', '1000', '10', 'AUD', '50', '10', '1050', '1050', '180', NULL, NULL, 'Lending'),
('21', 'H123123',  NULL, NULL, '4300', '1700', '9', 'SGD', '153', '17', '1853', '1853', '365', NULL, NULL, 'Lending'),
('22', 'H123123',  NULL, NULL, '90', '50', '4', 'DJF', '0.04', '0.5', '50.04', '50.04', '7', NULL, NULL, 'Lending'),
('23', 'H123123',  NULL, NULL, '500', '500', '10', 'AUD', '4.79', '5', '504.79', '504.79', '35', NULL, NULL, 'Lending'),
('24', 'H123123',  NULL, NULL, '1000', '1000', '10', 'AUD', '49.32', '10', '1049.32', '1049.32', '180', NULL, NULL, 'Lending'),
('25', 'H123123',  NULL, NULL, '15000', '6000', '8', 'HKD', '236.71', '60', '6236.71', '6236.71', '180', NULL, NULL, 'Lending'),
('26', 'H123123',  NULL, NULL, '300', '100', '12', 'BBD', '1.97', '1', '101.97', '101.97', '60', NULL, NULL, 'Lending'),
('27', 'A123456', NULL,'8000', '7000', '7000', NULL, 'CAD', NULL, '70', NULL, NULL, '365', NULL, NULL, 'Borrowing'),
('28', 'A123456', NULL,'5000', '2000', '2000', NULL, 'USD', NULL, '70', NULL, NULL, '50', NULL, NULL, 'Borrowing'),
('29', 'A123456', NULL,'100', '100', '100', NULL, 'CVE', NULL, '70', NULL, NULL, '10', NULL, NULL, 'Borrowing'),
('30', 'A123456', NULL,'1000', '700', '700', NULL, 'DKK', NULL, '70', NULL, NULL, '30', NULL, NULL, 'Borrowing'),
('31', 'A123456', NULL,'40000', '18000', '18000', NULL, 'CUP', NULL, '70', NULL, NULL, '500', NULL, NULL, 'Borrowing'),
('32', 'A123456', NULL,'10000', '6000', '6000', NULL, 'JOD', NULL, '70', NULL, NULL, '180', NULL, NULL, 'Borrowing');
COMMIT;
-- --------------------------------------------------------
-- Friends
-- Create database if it doesn't exist
-- Create database if it doesn't exist for "friends" table
CREATE DATABASE IF NOT EXISTS `lis_friend` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

-- Use the "friend" database
USE `lis_friend`;

-- Table structure for the "friends" table
DROP TABLE IF EXISTS `Friend`;
CREATE TABLE IF NOT EXISTS `Friend` (
    `fid` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `friend_id` VARCHAR(512),
    `friendee_id` VARCHAR(512),
    `friendee_name` VARCHAR(512)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

-- Insert values into the "friends" table
INSERT INTO `Friend` (friend_id, friendee_id, friendee_name) VALUES
('H123123', 'S9934651E', 'Derek'),
('H123123', 'A123456', 'Kanika'),
('A123456', 'H123123', 'Hui Min'),
('S9934651E', 'A123456', 'Kanika');

-- Commit the transaction
COMMIT;

