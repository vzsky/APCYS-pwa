-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 08, 2018 at 12:07 PM
-- Server version: 10.1.36-MariaDB
-- PHP Version: 7.0.32

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `APCYS`
--

-- --------------------------------------------------------

--
-- Table structure for table `announce`
--

CREATE TABLE `announce` (
  `id` int(40) NOT NULL,
  `topic` varchar(40) COLLATE utf8_bin NOT NULL,
  `content` varchar(300) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `announce`
--

INSERT INTO `announce` (`id`, `topic`, `content`) VALUES
(0, 'test webappp', 'test content sth abc lorem'),
(1, 'Posting', '....,.');

-- --------------------------------------------------------

--
-- Table structure for table `User`
--

CREATE TABLE `User` (
  `id` varchar(5) COLLATE utf8_bin NOT NULL,
  `Usr` varchar(20) COLLATE utf8_bin NOT NULL,
  `Pwd` varchar(20) COLLATE utf8_bin NOT NULL,
  `Name` varchar(100) COLLATE utf8_bin NOT NULL,
  `Residence` varchar(10) COLLATE utf8_bin NOT NULL,
  `PSRoom` varchar(10) COLLATE utf8_bin NOT NULL,
  `Country` varchar(20) COLLATE utf8_bin NOT NULL,
  `School` varchar(30) COLLATE utf8_bin NOT NULL,
  `SciAct` varchar(10) COLLATE utf8_bin NOT NULL,
  `PrjCode` varchar(10) COLLATE utf8_bin NOT NULL,
  `Bud1` varchar(100) COLLATE utf8_bin NOT NULL,
  `Bud2` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `Bud3` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `Bud4` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `S1` varchar(1) COLLATE utf8_bin DEFAULT NULL,
  `S2` varchar(1) COLLATE utf8_bin DEFAULT NULL,
  `S3` varchar(1) COLLATE utf8_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `User`
--

INSERT INTO `User` (`id`, `Usr`, `Pwd`, `Name`, `Residence`, `PSRoom`, `Country`, `School`, `SciAct`, `PrjCode`, `Bud1`, `Bud2`, `Bud3`, `Bud4`, `S1`, `S2`, `S3`) VALUES
('0', 'admin', 'root', 'Administrator', 'cloud', 'https', 'World', 'KVIS', 'Organizer', '000', 'Adbud1', 'AdBud2', 'AdBud3', 'AdBud4', NULL, NULL, NULL),
('1', 'username', 'password', 'First Last', '1445', '321', 'Thailand', 'KVIS', 'gamma', '001', 'mybud1', 'myBud2', 'myBud3', 'myBud4', NULL, NULL, NULL),
('50', 'Fido', 'fido', 'TamaraLynn', 'B3', '3002', 'ENG', 'Hogwarts', 'CHE', '5001', 'Barry', 'Harry', NULL, NULL, NULL, NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `announce`
--
ALTER TABLE `announce`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `User`
--
ALTER TABLE `User`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `Usr` (`Usr`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
