DROP DATABASE IF EXISTS lendinsync;
CREATE DATABASE lendinsync;

USE lendinsync;

CREATE TABLE lendinsync.Wallet 
(
    WID INT NOT NULL PRIMARY KEY,
    CustomerId VARCHAR(512),
    CurrencyCode VARCHAR(512),
    Amount MONEY
)ENGINE = InnoDB;

INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('1', 'A123456', 'VND', '2,725,451');
INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('2', 'A123456', 'USD', '97.61');
INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('3', 'A123456', 'AUD', '174.943');
INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('4', 'A123456', 'BBD', '202.955');
INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('5', 'A123456', 'JPY', '25,723.80');
INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('6', 'S9934651E', 'NZD', '298.138');
INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('7', 'S9934651E', 'USD', '173.753');
INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('8', 'S9934651E', 'AED', '710.489');
INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('9', 'S9934651E', 'CHF', '173.132');
INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('10', 'S9934651E', 'KYD', '182.513');
INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('11', 'H123123', 'CAD', '301.572');
INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('12', 'H123123', 'BND', '312');
INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('13', 'H123123', 'CNY', '1,601.89');
INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('14', 'H123123', 'ISK', '27,884.70');
INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('15', 'H123123', 'INR', '16,688.40');
INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('16', 'H123123', 'USD', '154.89');
INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('17', 'S9934651E', 'JPY', '27,037.40');
INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('18', 'A123456', 'KWD', '33.7801');
INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('19', 'S9934651E', 'MYR', '523.182');
INSERT INTO tableName (WID, CustomerId, CurrencyCode, Amount) VALUES ('20', 'H123123', 'NZD', '202.934');


CREATE TABLE lendinsync.Transaction 
(
    TID INT NOT NULL PRIMARY KEY,
    SourceWallet INT,
    DestinationWallet INT,
    CustomerId VARCHAR(512),
    AmountTransferred MONEY,
    WalletTransaction BOOLEAN,
    ExchangeRate MONEY,
    TimeStamp TIMESTAMP
)ENGINE = InnoDB;

INSERT INTO tableName (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES ('1', '1', '4', 'A123456', '50,000', 'TRUE', '0.00008', '2023-04-10 10:39:37');
INSERT INTO tableName (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES ('2', '3', '5', 'A123456', '50', 'TRUE', '95.0925', '2023-05-11 09:39:37');
INSERT INTO tableName (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES ('3', '5', '2', 'A123456', '10,000', 'TRUE', '0.00667', '2023-03-15 10:39:37');
INSERT INTO tableName (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES ('4', '4', '5', 'A123456', '150.85', 'TRUE', '74.969', '2023-09-01 10:19:36');
INSERT INTO tableName (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES ('5', '2', '5', 'A123456', '75', 'TRUE', '149.938', '2023-04-10 10:39:37');
INSERT INTO tableName (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES ('6', '4', '1', 'A123456', '120', 'TRUE', '12,280.40', '2023-07-19 10:39:37');
INSERT INTO tableName (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES ('7', '1', '', 'A123456', '1200000', 'FALSE', '0.00006', '2023-04-10 10:39:37');
INSERT INTO tableName (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES ('8', '2', '', 'A123456', '20', 'FALSE', '1.36957', '2023-04-10 10:39:37');
INSERT INTO tableName (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES ('9', '', '4', 'A123456', '50', 'FALSE', '1.46011', '2023-04-10 10:39:37');
INSERT INTO tableName (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES ('10', '', '5', 'A123456', '45', 'FALSE', '109.463', '2023-04-10 10:39:37');
INSERT INTO tableName (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES ('11', '6', '7', 'S9934651E', '123.5', 'TRUE', '0.58264', '2023-04-10 10:39:37');
INSERT INTO tableName (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES ('12', '7', '8', 'S9934651E', '85.7', 'TRUE', '3.67246', '2023-04-10 10:39:37');
INSERT INTO tableName (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES ('13', '8', '9', 'S9934651E', '350.6', 'TRUE', '0.24361', '2023-04-10 10:39:37');
INSERT INTO tableName (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES ('14', '9', '10', 'S9934651E', '56.8', 'TRUE', '0.93102', '2023-04-10 10:39:37');
INSERT INTO tableName (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES ('15', '7', '', 'S9934651E', '65', 'FALSE', '1.36957', '2023-04-10 10:39:37');
INSERT INTO tableName (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES ('16', '9', '', 'S9934651E', '100.45', 'FALSE', '1.53011', '2023-04-10 10:39:37');
INSERT INTO tableName (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES ('17', '', '6', 'S9934651E', '67', 'FALSE', '1.25268', '2023-04-10 10:39:37');
INSERT INTO tableName (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES ('18', '', '9', 'S9934651E', '30', 'FALSE', '0.65333', '2023-04-10 10:39:37');
INSERT INTO tableName (TID, SourceWallet, DestinationWallet, CustomerId, AmountTransferred, WalletTransaction, ExchangeRate, TimeStamp) VALUES ('19', '', '10', 'S9934651E', '105', 'FALSE', '0.60838', '2023-04-10 10:39:37');


CREATE TABLE lendinsync.Loan 
(
    LoanId INT NOT NULL PRIMARY KEY,
    CustomerId VARCHAR(512),
    CollateralAmount MONEY,
    LoanAmount	MONEY,
    InvestmentAmount MONEY,
    InterestRate	PERCENTAGE,
    CurrencyCode 	VARCHAR(512),
    TotalInterestAmount	INT,
    ServiceFee	MONEY,
    RepaymentAmount	MONEY,
    Revenue MONEY,
    LoanTerm INT,
    StartDate TIMESTAMP,
    EndDate TIMESTAMP,
    StatusLevel	VARCHAR(512),
    StatusTypes	VARCHAR(512),
)ENGINE = InnoDB;

INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('1', 'A123456', '1000', '800', '', '10', 'USD', '80', '50', '930', '', '365', '2023-10-15 10:39:37', '2024-10-14 10:39:37', 'BMatch', '', 'Borrowing', '');
INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('2', 'S9934651E', '', '', '800', '10', 'USD', '80', '50', '', '80', '365', '2022-12-27 09:39:37', '2023-12-27 09:39:37', 'LMatch', '', 'Lending', '');
INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('3', 'H123123', '500', '400', '', '11', 'NZD', '40', '20', '460', '', '365', '2023-09-23 10:39:37', '2024-09-22 10:39:37', 'Borrowing', '', 'Closed', 'Will not be shown in the lending marketplace');
INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('4', 'A123456', '1500', '1200', '', '12', 'USD', '144', '30', '1344', '', '365', '2022-08-10 10:39:37', '2023-08-10 10:39:37', 'Closed', '', 'BMatch', '');
INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('5', 'A123456', '', '', '1000', '10', 'AED', '50', '10', '', '50', '180', '2023-10-12 10:39:37', '2024-04-09 10:39:37', 'Lending', '', 'LMatch', '');
INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('6', 'A123456', '', '', '5000', '11', 'CHF', '400', '30', '', '400', '270', '2022-09-07 10:39:37', '2023-06-04 10:39:37', 'Closed', '', '', '');
INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('7', 'A123456', '10000', '7000', '', '10', 'KYD', '700', '50', '7750', '', '365', '2023-09-11 10:39:37', '2024-09-10 10:39:37', 'Borrowing', '', '', '');
INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('8', 'A123456', '1000', '750', '', '10', 'VND', '12', '10', '772', '', '90', '2023-03-05 10:39:37', '2023-06-03 10:39:37', 'Closed', '', '', '');
INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('9', 'A123456', '', '', '2000', '10', 'USD', '100', '30', '', '100', '180', '2023-08-12 10:39:37', '2024-02-08 10:39:37', 'BMatch', '', '', '');
INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('10', 'S9934651E', '', '', '5000', '10', 'AUD', '500', '40', '', '500', '365', '2023-10-18 10:39:37', '2024-10-17 10:39:37', 'Lending', '', '', '');
INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('11', 'S9934651E', '', '', '10000', '11', 'BBD', '1100', '50', '', '1100', '365', '2023-09-11 10:39:37', '2024-09-10 10:39:37', 'Lending', '', '', '');
INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('12', 'S9934651E', '', '', '20000', '12', 'JPY', '2400', '60', '', '2400', '365', '2023-10-10 10:39:37', '2024-10-09 10:39:37', 'Lending', '', '', '');
INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('13', 'S9934651E', '5000', '3500', '', '10', 'KYD', '175', '30', '3705', '', '180', '2023-10-20 10:39:37', '2024-04-17 10:39:37', 'Borrowing', '', '', '');
INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('14', 'S9934651E', '1000', '750', '', '11', 'VND', '42', '20', '812', '', '180', '2023-10-24 10:39:37', '2024-04-21 10:39:37', 'Borrowing', '', '', '');
INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('15', 'S9934651E', '1000', '800', '', '10', 'USD', '14', '20', '834', '', '90', '2023-05-10 10:39:37', '2023-08-08 10:39:37', 'Closed', '', '', '');
INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('16', 'H123123', '500', '350', '', '10', 'AUD', '5', '10', '365', '', '90', '2023-04-12 10:39:37', '2023-07-11 10:39:37', 'Closed', '', '', '');
INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('17', 'H123123', '2000', '1600', '', '11', 'BBD', '85', '20', '1705', '', '180', '2023-10-19 10:39:37', '2024-04-16 10:39:37', 'LMatch', '', '', '');
INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('18', 'H123123', '', '', '1000', '10', 'VND', '50', '10', '', '50', '180', '2023-10-26 10:39:37', '2024-04-23 10:39:37', 'Lending', '', '', '');
INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('19', 'H123123', '', '', '2000', '9', 'USD', '90', '20', '', '90', '180', '2023-02-10 10:39:37', '2023-08-09 10:39:37', 'Closed', '', '', '');
INSERT INTO tableName (LoanId, CustomerId, CollateralAmount, LoanAmount, InvestmentAmount, InterestRate, CurrencyCode , TotalInterestAmount, ServiceFee, RepaymentAmount, Revenue, LoanTerm, StartDate, EndDate, StatusLevel, , StatusTypes, ) VALUES ('20', 'H123123', '', '', '5000', '12', 'AUD', '600', '20', '', '600', '365', '2023-10-12 10:39:37', '2024-10-11 10:39:37', 'Lending');