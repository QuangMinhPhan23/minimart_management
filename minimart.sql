

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `minimart`
--

-- --------------------------------------------------------

--
-- `login` table structure
--

DROP TABLE IF EXISTS `login`;
CREATE TABLE IF NOT EXISTS `login` (
  `ordinal_num` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `account_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`ordinal_num`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Insert data to `login`
--

INSERT INTO `login` (`ordinal_num`, `account_name`, `password`) VALUES
(1, 'quangminh', '123456');

-- --------------------------------------------------------

--
-- `product` table structure
--

DROP TABLE IF EXISTS `product`;
CREATE TABLE IF NOT EXISTS `product` (
  `ordinal_num` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `product_id` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `product_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `origin` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `image` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `available_quantity` int(15) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`ordinal_num`,`product_id`)
) ENGINE=MyISAM AUTO_INCREMENT=51 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Insert data to `product`
--

INSERT INTO `product` (`ordinal_num`, `product_id`, `product_name`, `origin`, `image`,  `available_quantity`) VALUES
(50, 'SP0021', 'Pin C', 'Mi', 'p.jpg', 100),
(49, 'SP020', 'Xa phong Bluestones', 'Nhat', 'xp.jpg', 100),
(48, 'SP019', 'Kem đanh rang Sunhouse', 'Mi', 'kdr.jpg', 100),
(47, 'SP018', 'Nuoc suc mieng Bluestones', 'Han', 'nsm.jpg', 100),
(46, 'SP017', 'Xa phong Sunhouse', 'Han', 'xp.jpg', 100),
(45, 'SP016', 'Ban chai Philips', 'Anh', 'bc.jpg', 100),
(44, 'SP015', 'Kem đanh rang Philips', 'Trung Quoc', 'kdr.jpg', 100),
(43, 'SP014', 'Kem đanh rang Philips', 'Anh', 'kdr.jpg', 100),
(42, 'SP013', 'Ban chai SATO', 'Anh', 'bc.jpg', 100),
(41, 'SP012', 'Xa phong Philips', 'Viet Nam', 'xp.jpg', 100),
(40, 'SP011', 'Nuoc suc mieng Philips', 'Mi', 'nsm.jpg', 100),
(39, 'SP010', 'Chao Kangaroo', 'Phap', 'c.jpg', 100),
(38, 'SP009', 'Chao Sunhouse', 'Viet Nam', 'c.jpg', 100),
(37, 'SP008', 'Ban chai Sunhouse', 'Mi', 'bc.jpg', 100),
(36, 'SP007', 'Nuoc suc mieng SATO', 'Phap', 'nsm.jpg', 100),
(35, 'SP006', 'Kem đanh rang Goldsun', 'Anh', 'kdr.jpg', 100),
(34, 'SP005', 'Ban chai SATO', 'Viet Nam', 'bc.jpg', 100),
(33, 'SP004', 'Ban chai Sunhouse', 'Trung Quoc', 'bc.jpg', 100),
(32, 'SP003', 'Nuoc suc mieng Kangaroo', 'Mi', 'nsm.jpg', 100),
(31, 'SP002', 'Pin Goldsun', 'Trung Quoc', 'p.jpg', 100),
(30, 'SP001', 'Pin Sunhouse', 'Phap', 'p.jpg', 100);

-- --------------------------------------------------------

--
-- `quotation` table structure
--

DROP TABLE IF EXISTS `quotation`;
CREATE TABLE IF NOT EXISTS `quotation` (
  `ordinal_num` int(11) NOT NULL AUTO_INCREMENT,
  `price_id` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `product_id` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `Price` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `Applied_date` date NOT NULL,
  `supplier` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`ordinal_num`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Insert data to `quotation`
--

INSERT INTO `quotation` (`ordinal_num`, `price_id`, `product_id`, `Price`, `Applied_date`,`supplier`) VALUES
(1, 'IP001', 'SP001', '25000', '2023-02-15','NKT'),
(2, 'IP002', 'SP002', '90000', '2023-02-14','NKT'),
(3, 'IP003', 'SP003', '18000', '2023-02-08','NKT'),
(4, 'IP004', 'SP004', '32000', '2023-02-20','NKT'),
(5, 'IP003', 'SP003', '18000', '2023-02-08','NKT'),
(6, 'IP004', 'SP004', '32000', '2023-02-20','NKT'),
(7, 'IP005', 'SP005', '40000', '2023-02-09','NKT'),
(8, 'IP005', 'SP005', '64000', '2023-02-23','NKT');

-- --------------------------------------------------------

--
-- `selling` table structure
--

DROP TABLE IF EXISTS `selling`;
CREATE TABLE IF NOT EXISTS `selling` (
  `ordinal_num` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `date` date NOT NULL,
  `Amount` int(20) NOT NULL,
  PRIMARY KEY (`ordinal_num`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- `staff` table structure
--

DROP TABLE IF EXISTS `staff`;
CREATE TABLE IF NOT EXISTS `staff` (
  `ordinal_num` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `staff_id` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `staff_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `date_of_birth` date NOT NULL,
  `gender` tinyint(1) NOT NULL,
  `identification` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `mobile_phone` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `image` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`ordinal_num`,`staff_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Insert data to `staff`
--

INSERT INTO `staff` (`ordinal_num`, `staff_id`, `staff_name`, `date_of_birth`, `gender`, `identification`, `mobile_phone`, `image`) VALUES
(1, 'NV001', 'Nguyen Quoc Hai', '1995-02-10', 1, '2334586283', '0865019420', 'h6.jpg'),
(2, 'NV002', 'Tran Van Tuan', '2000-09-16', 1, '2521075458', '0139570676', 'h1.jpg'),
(3, 'NV003', 'Le Huu Quang', '1991-02-25', 1, '2903704636', '0575310976', 'h6.jpg'),
(4, 'NV004', 'Le Tien Quoc', '1972-07-05', 1, '2931141980', '0650590646', 'h3.jpg'),
(5, 'NV005', 'Ngo Van Hung', '1972-07-11', 1, '2313950701', '0923085277', 'h4.jpg'),
(7, 'SV006', 'Phan Viet Hai', '1980-01-09', 1, '1231142342', '0312132312', 'h5.jpg');
COMMIT;


