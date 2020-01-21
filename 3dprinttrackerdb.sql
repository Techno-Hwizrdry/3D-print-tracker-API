-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jan 20, 2020 at 06:57 PM
-- Server version: 10.1.38-MariaDB-0+deb9u1
-- PHP Version: 7.0.33-0+deb9u6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `3dprinttrackerdb`
--
CREATE DATABASE IF NOT EXISTS `3dprinttrackerdb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `3dprinttrackerdb`;

-- --------------------------------------------------------

--
-- Table structure for table `3dprints`
--

CREATE TABLE `3dprints` (
  `id` int(10) UNSIGNED NOT NULL,
  `filename` text NOT NULL COMMENT 'Filename of the 3D print.',
  `print_count` int(10) UNSIGNED NOT NULL COMMENT 'How many times has this file been printed.',
  `print_time` float UNSIGNED NOT NULL COMMENT 'How many hours it takes to print.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `print_datetimes`
--

CREATE TABLE `print_datetimes` (
  `id` int(10) UNSIGNED NOT NULL COMMENT 'Used for selecting the most recent print.',
  `id_3dprint` int(10) UNSIGNED NOT NULL COMMENT 'Refers to id in 3dprints table.',
  `start_datetime` datetime NOT NULL COMMENT 'What date and time the print job started.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `3dprints`
--
ALTER TABLE `3dprints`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `print_datetimes`
--
ALTER TABLE `print_datetimes`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `3dprints`
--
ALTER TABLE `3dprints`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `print_datetimes`
--
ALTER TABLE `print_datetimes`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Used for selecting the most recent print.';
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
