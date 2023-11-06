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
('1', '1', '4', 'A123456', '50000', 'TRUE', '0.00008', '2023-04-10 10:39:37'),
('2', '3', '5', 'A123456', '50', 'TRUE', '95.0925', '2023-05-11 09:39:37'),
('3', '5', '2', 'A123456', '10000', 'TRUE', '0.00667', '2023-03-15 10:39:37'),
('4', '4', '5', 'A123456', '150.85', 'TRUE', '74.969', '2023-09-01 10:19:36'),
('5', '2', '5', 'A123456', '75', 'TRUE', '149.938', '2023-04-10 10:39:37'),
('6', '4', '1', 'A123456', '120', 'TRUE', '12280.40', '2023-07-19 10:39:37'),
('7', '1', NULL, 'A123456', '1200000', 'FALSE', '0.00006', '2023-04-10 10:39:37'),
('8', '2', NULL, 'A123456', '20', 'FALSE', '1.36957', '2023-04-10 10:39:37'),
('9', NULL, '4', 'A123456', '50', 'FALSE', '1.46011', '2023-04-10 10:39:37'),
('10', NULL, '5', 'A123456', '45', 'FALSE', '109.463', '2023-04-10 10:39:37'),
('11', '6', '7', 'S9934651E', '123.5', 'TRUE', '0.58264', '2023-04-10 10:39:37'),
('12', '7', '8', 'S9934651E', '85.7', 'TRUE', '3.67246', '2023-04-10 10:39:37'),
('13', '8', '9', 'S9934651E', '350.6', 'TRUE', '0.24361', '2023-04-10 10:39:37'),
('14', '9', '10', 'S9934651E', '56.8', 'TRUE', '0.93102', '2023-04-10 10:39:37'),
('15', '7', NULL, 'S9934651E', '65', 'FALSE', '1.36957', '2023-04-10 10:39:37'),
('16', '9', NULL, 'S9934651E', '100.45', 'FALSE', '1.53011', '2023-04-10 10:39:37'),
('17', NULL, '6', 'S9934651E', '67', 'FALSE', '1.25268', '2023-04-10 10:39:37'),
('18', NULL, '9', 'S9934651E', '30', 'FALSE', '0.65333', '2023-04-10 10:39:37'),
('19', NULL, '10', 'S9934651E', '105', 'FALSE', '0.60838', '2023-04-10 10:39:37');
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
('1', 'A123456', 'S9934651E','1000', '800', NULL, '10', 'USD', '80', '50', '930', NULL, '365', '2023-10-15 10:39:37', '2024-10-14 10:39:37', 'BMatch'),
('2', 'S9934651E', 'H123123', NULL, NULL, '800', '10', 'USD', '80', '50', NULL, '80', '365', '2022-12-27 09:39:37', '2023-12-27 09:39:37', 'LMatch'),
('3', 'H123123', NULL,'500', '400', NULL, '11', 'NZD', '40', '20', '460', NULL, '365', '2023-09-23 10:39:37', '2024-09-22 10:39:37', 'Borrowing'),
('4', 'A123456', NULL,'1500', '1200', NULL, '12', 'USD', '144', '30', '1344', NULL, '365', '2022-08-10 10:39:37', '2023-08-10 10:39:37', 'Closed'),
('5', 'A123456', NULL,NULL, NULL, '1000', '10', 'AED', '50', '10', NULL, '50', '180', '2023-10-12 10:39:37', '2024-04-09 10:39:37', 'Lending'),
('6', 'A123456', NULL,NULL, NULL, '5000', '11', 'CHF', '400', '30', NULL, '400', '270', '2022-09-07 10:39:37', '2023-06-04 10:39:37', 'Closed'),
('7', 'A123456', NULL,'10000', '7000', NULL, '10', 'KYD', '700', '50', '7750', NULL, '365', '2023-09-11 10:39:37', '2024-09-10 10:39:37', 'Borrowing'),
('8', 'A123456', NULL,'1000', '750', NULL, '10', 'VND', '12', '10', '772', NULL, '90', '2023-03-05 10:39:37', '2023-06-03 10:39:37', 'Closed'),
('9', 'A123456', 'S9934651E', NULL, NULL, '2000', '10', 'USD', '100', '30', NULL, '100', '180', '2023-08-12 10:39:37', '2024-02-08 10:39:37', 'BMatch'),
('10', 'S9934651E', NULL,NULL, NULL, '5000', '10', 'AUD', '500', '40', NULL, '500', '365', '2023-10-18 10:39:37', '2024-10-17 10:39:37', 'Lending'),
('11', 'S9934651E', NULL,NULL, NULL, '10000', '11', 'BBD', '1100', '50', NULL, '1100', '365', '2023-09-11 10:39:37', '2024-09-10 10:39:37', 'Lending'),
('12', 'S9934651E', NULL,NULL, NULL, '20000', '12', 'JPY', '2400', '60', NULL, '2400', '365', '2023-10-10 10:39:37', '2024-10-09 10:39:37', 'Lending'),
('13', 'S9934651E', NULL,'5000', '3500', NULL, '10', 'KYD', '175', '30', '3705', NULL, '180', '2023-10-20 10:39:37', '2024-04-17 10:39:37', 'Borrowing'),
('14', 'S9934651E', NULL,'1000', '750', NULL, '11', 'VND', '42', '20', '812', NULL, '180', '2023-10-24 10:39:37', '2024-04-21 10:39:37', 'Borrowing'),
('15', 'S9934651E', NULL,'1000', '800', NULL, '10', 'USD', '14', '20', '834', NULL, '90', '2023-05-10 10:39:37', '2023-08-08 10:39:37', 'Closed'),
('16', 'H123123', NULL,'500', '350', NULL, '10', 'AUD', '5', '10', '365', NULL, '90', '2023-04-12 10:39:37', '2023-07-11 10:39:37', 'Closed'),
('17', 'H123123', 'S9934651E','2000', '1600', NULL, '11', 'BBD', '85', '20', '1705', NULL, '180', '2023-10-19 10:39:37', '2024-04-16 10:39:37', 'LMatch'),
('18', 'H123123', NULL,NULL, NULL, '1000', '10', 'VND', '50', '10', NULL, '50', '180', '2023-10-26 10:39:37', '2024-04-23 10:39:37', 'Lending'),
('19', 'H123123', NULL,NULL, NULL, '2000', '9', 'USD', '90', '20', NULL, '90', '180', '2023-02-10 10:39:37', '2023-08-09 10:39:37', 'Closed'),
('20', 'H123123', NULL,NULL, NULL, '5000', '12', 'AUD', '600', '20', NULL, '600', '365', '2023-10-12 10:39:37', '2024-10-11 10:39:37', 'Lending');
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

