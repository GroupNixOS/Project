-- MySQL dump 10.13  Distrib 5.7.24, for osx11.1 (x86_64)
--
-- Host: localhost    Database: proj
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `freq`
--

DROP TABLE IF EXISTS `freq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `freq` (
  `ID` varchar(15) DEFAULT NULL,
  `Population` varchar(3) DEFAULT NULL,
  `Genotype_0` decimal(4,3) DEFAULT NULL,
  `Genotype_1` decimal(4,3) DEFAULT NULL,
  `Genotype_2` decimal(4,3) DEFAULT NULL,
  `Ref` decimal(4,3) DEFAULT NULL,
  `Alt` decimal(4,3) DEFAULT NULL,
  KEY `fk_metadata` (`ID`),
  KEY `fk_pop` (`Population`),
  CONSTRAINT `fk_metadata` FOREIGN KEY (`ID`) REFERENCES `metadata` (`ID`),
  CONSTRAINT `fk_pop` FOREIGN KEY (`Population`) REFERENCES `pop` (`Population`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `metadata`
--

DROP TABLE IF EXISTS `metadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `metadata` (
  `POS` int DEFAULT NULL,
  `ID` varchar(20) NOT NULL,
  `REF` varchar(1) DEFAULT NULL,
  `ALT` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pca`
--

DROP TABLE IF EXISTS `pca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pca` (
  `Population` varchar(3) DEFAULT NULL,
  `PC1` decimal(30,20) DEFAULT NULL,
  `PC2` decimal(30,20) DEFAULT NULL,
  `PC3` decimal(30,20) DEFAULT NULL,
  `PC4` decimal(30,20) DEFAULT NULL,
  `PC5` decimal(30,20) DEFAULT NULL,
  `PC6` decimal(30,20) DEFAULT NULL,
  `PC7` decimal(30,20) DEFAULT NULL,
  `PC8` decimal(30,20) DEFAULT NULL,
  `PC9` decimal(30,20) DEFAULT NULL,
  `PC10` decimal(30,20) DEFAULT NULL,
  `PC11` decimal(30,20) DEFAULT NULL,
  `PC12` decimal(30,20) DEFAULT NULL,
  `PC13` decimal(30,20) DEFAULT NULL,
  `PC14` decimal(30,20) DEFAULT NULL,
  `PC15` decimal(30,20) DEFAULT NULL,
  `PC16` decimal(30,20) DEFAULT NULL,
  `PC17` decimal(30,20) DEFAULT NULL,
  `PC18` decimal(30,20) DEFAULT NULL,
  `PC19` decimal(30,20) DEFAULT NULL,
  `PC20` decimal(30,20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pop`
--

DROP TABLE IF EXISTS `pop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pop` (
  `Sample` varchar(20) NOT NULL,
  `Population` varchar(3) DEFAULT NULL,
  `Superpopulation` varchar(3) DEFAULT NULL,
  PRIMARY KEY (`Sample`),
  KEY `idx_Population` (`Population`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pve`
--

DROP TABLE IF EXISTS `pve`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pve` (
  `PC1` decimal(30,20) DEFAULT NULL,
  `PC2` decimal(30,20) DEFAULT NULL,
  `PC3` decimal(30,20) DEFAULT NULL,
  `PC4` decimal(30,20) DEFAULT NULL,
  `PC5` decimal(30,20) DEFAULT NULL,
  `PC6` decimal(30,20) DEFAULT NULL,
  `PC7` decimal(30,20) DEFAULT NULL,
  `PC8` decimal(30,20) DEFAULT NULL,
  `PC9` decimal(30,20) DEFAULT NULL,
  `PC10` decimal(30,20) DEFAULT NULL,
  `PC11` decimal(30,20) DEFAULT NULL,
  `PC12` decimal(30,20) DEFAULT NULL,
  `PC13` decimal(30,20) DEFAULT NULL,
  `PC14` decimal(30,20) DEFAULT NULL,
  `PC15` decimal(30,20) DEFAULT NULL,
  `PC16` decimal(30,20) DEFAULT NULL,
  `PC17` decimal(30,20) DEFAULT NULL,
  `PC18` decimal(30,20) DEFAULT NULL,
  `PC19` decimal(30,20) DEFAULT NULL,
  `PC20` decimal(30,20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-07 17:16:43