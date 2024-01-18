-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 18, 2024 at 11:09 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `finance_manager_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `cards`
--

CREATE TABLE `cards` (
  `user_name` varchar(25) NOT NULL,
  `card_num` varchar(20) NOT NULL,
  `card_name` varchar(200) NOT NULL,
  `phn_num` varchar(10) NOT NULL,
  `cvv_num` varchar(6) NOT NULL,
  `pin_num` varchar(8) NOT NULL,
  `bank_name` varchar(255) NOT NULL,
  `card_type` varchar(8) NOT NULL,
  `total_limit` int(20) NOT NULL,
  `used_limit` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cards`
--

INSERT INTO `cards` (`user_name`, `card_num`, `card_name`, `phn_num`, `cvv_num`, `pin_num`, `bank_name`, `card_type`, `total_limit`, `used_limit`) VALUES
('qwerty', '0987654321', 'MM Corporation', '918273645', '432', '0987', 'HDFC', 'Credit', 100000, 90000),
('qwerty', '123456789', 'MM Industries', '9876543210', '123', '1234', 'SBI', 'Debit', 50000, 27500),
('qwerty', '1324576890', 'MM LLC', '987563421', '987', '876', 'UBI', 'Credit', 80000, 45000),
('qwerty', '2345678910', 'MM Registered', '567890123', '456', '65', 'Kotak', 'Debit', 75000, 0),
('qwerty', '5647382910', 'MM Company', '0987654321', '789', '654', 'ICICI', 'Debit', 30000, 0),
('qwerty', '6565', 'HEHE', '123', '1', '23', 'RBI', 'Debit', 1000, 0),
('qwerty', '7890654321', 'MM Legal', '76854321', '987', '456', 'AU Small', 'Credit', 45000, 0);

-- --------------------------------------------------------

--
-- Table structure for table `loan`
--

CREATE TABLE `loan` (
  `user_name` varchar(25) NOT NULL,
  `application_number` int(20) NOT NULL,
  `type` varchar(100) NOT NULL,
  `amount` int(20) NOT NULL,
  `period` int(20) NOT NULL,
  `interest` int(20) NOT NULL,
  `emi` int(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `loan`
--

INSERT INTO `loan` (`user_name`, `application_number`, `type`, `amount`, `period`, `interest`, `emi`) VALUES
('qwerty', 0, 'home', 1000000, 10, 8, 12132),
('qwerty', 123, 'qw', 12, 1, 2, 1),
('qwerty', 1230, 'home', 987, 2, 3, 42);

-- --------------------------------------------------------

--
-- Table structure for table `mutual_fund`
--

CREATE TABLE `mutual_fund` (
  `user_name` varchar(25) NOT NULL,
  `fund_name` varchar(200) NOT NULL,
  `goal` varchar(300) NOT NULL,
  `price` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mutual_fund`
--

INSERT INTO `mutual_fund` (`user_name`, `fund_name`, `goal`, `price`) VALUES
('qwerty', 'Axis', 'car', 1000);

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

CREATE TABLE `notification` (
  `user_name` varchar(25) NOT NULL,
  `amount` int(20) NOT NULL,
  `due_date` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notification`
--

INSERT INTO `notification` (`user_name`, `amount`, `due_date`) VALUES
('qwerty', 10000, 'After 2 days');

-- --------------------------------------------------------

--
-- Table structure for table `other_investment`
--

CREATE TABLE `other_investment` (
  `user_name` varchar(25) NOT NULL,
  `investment` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `stocks`
--

CREATE TABLE `stocks` (
  `user_name` varchar(25) NOT NULL,
  `stock_name` varchar(100) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `ticker_name` varchar(100) NOT NULL,
  `p_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stocks`
--

INSERT INTO `stocks` (`user_name`, `stock_name`, `quantity`, `price`, `ticker_name`, `p_id`) VALUES
('qwerty', 'amazon', 123, 145, 'AMZ', '1234567'),
('qwerty', 'amazon', 133, 456, 'AMZ', '332377'),
('qwerty', 'amazon', 20, 678, 'AMZ', '332452'),
('qwerty', 'amazon', 133, 456, 'AMZ', '446621'),
('qwerty', 'tata', 123, 2000, 'TCS.NS', '446767'),
('qwerty', 'apple', 100, 101, 'AAPL', '460074'),
('qwerty', 'microsoft', 50, 330, 'MSFT', '460142'),
('qwerty', 'Amazon', 110, 1245, 'AMZ', '7654321'),
('qwerty', '', 0, 0, '', '792204');

-- --------------------------------------------------------

--
-- Table structure for table `subscription`
--

CREATE TABLE `subscription` (
  `user_name` varchar(25) NOT NULL,
  `name` varchar(100) NOT NULL,
  `genre` varchar(100) NOT NULL,
  `charges` varchar(100) NOT NULL,
  `plan_date` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `subscription`
--

INSERT INTO `subscription` (`user_name`, `name`, `genre`, `charges`, `plan_date`) VALUES
('qwerty', '90', 'op', '13', 'monthly'),
('qwerty', 'amazon', 'enter', '1500', 'yearly'),
('qwerty', 'awe', 'we', '120', 'yearly'),
('qwerty', 'ewq', 'qwer', '123', 'yearly'),
('qwerty', 'hey hey', 'nothing', '123', 'yearly'),
('qwerty', 'jhn', 'mkl', '20', 'yearly'),
('qwerty', 'k', 'poi', '18', 'yearly'),
('qwerty', 'kl', 'lk', '11', 'yearly'),
('qwerty', 'lkjh', 'nm', '18', 'yearly'),
('qwerty', 'lop', 'vbbn', '34', 'yearly'),
('qwerty', 'm', 'b', '10', 'yearly'),
('qwerty', 'mn', 'io', '14', 'weekly'),
('qwerty', 'nb', 'kl', '15', 'weekly'),
('qwerty', 'Netflix', 'entertainment', '180', 'weekly'),
('qwerty', 'op', 'po', '12', 'weekly'),
('qwerty', 'q', 'w', '1', 'weekly'),
('qwerty', 'qq', 'qe', '7', 'weekly'),
('qwerty', 'w', 'e', '2', 'weekly'),
('qwerty', 'z', 'x', '5', 'weekly');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `user_name` varchar(25) NOT NULL,
  `merchant_name` varchar(200) CHARACTER SET armscii8 COLLATE armscii8_bin NOT NULL,
  `date` date NOT NULL,
  `card_number` varchar(20) NOT NULL,
  `card_type` varchar(20) NOT NULL,
  `amount` int(30) NOT NULL,
  `payment_id` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`user_name`, `merchant_name`, `date`, `card_number`, `card_type`, `amount`, `payment_id`) VALUES
('qwerty', 'Apple', '2020-03-01', '0987654321', 'Credit', 90000, '100161'),
('qwerty', 'a', '0000-00-00', '123456789', 'q', 2000, '1691870844'),
('qwerty', 'Samsung', '0000-00-00', '123456789', 'Credit', 3500, '372259'),
('qwerty', 'Samsung', '2023-08-18', '123456789', 'Credit', 2000, '372589'),
('qwerty', 'Nothing', '2023-08-18', '1324576890', 'Credit', 45000, '373252'),
('qwerty', 'apple', '2020-09-08', '123456789', 'c', 12000, '95299'),
('qwerty', 'a', '0000-00-00', '123456789', 's', 6000, '953054');

-- --------------------------------------------------------

--
-- Table structure for table `user_table`
--

CREATE TABLE `user_table` (
  `user_name` varchar(25) NOT NULL,
  `e_id` varchar(30) NOT NULL,
  `password` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_table`
--

INSERT INTO `user_table` (`user_name`, `e_id`, `password`) VALUES
('jatin', 'jatin@mail', 'abara'),
('qwerty', 'poiu', 'abara'),
('user', 'id@mail', 'abara');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cards`
--
ALTER TABLE `cards`
  ADD PRIMARY KEY (`card_num`);

--
-- Indexes for table `loan`
--
ALTER TABLE `loan`
  ADD PRIMARY KEY (`application_number`);

--
-- Indexes for table `mutual_fund`
--
ALTER TABLE `mutual_fund`
  ADD PRIMARY KEY (`user_name`);

--
-- Indexes for table `notification`
--
ALTER TABLE `notification`
  ADD PRIMARY KEY (`user_name`);

--
-- Indexes for table `other_investment`
--
ALTER TABLE `other_investment`
  ADD PRIMARY KEY (`user_name`);

--
-- Indexes for table `stocks`
--
ALTER TABLE `stocks`
  ADD PRIMARY KEY (`p_id`);

--
-- Indexes for table `subscription`
--
ALTER TABLE `subscription`
  ADD PRIMARY KEY (`name`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`payment_id`);

--
-- Indexes for table `user_table`
--
ALTER TABLE `user_table`
  ADD PRIMARY KEY (`user_name`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
