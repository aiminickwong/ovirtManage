-- MySQL dump 10.13  Distrib 5.6.36, for Linux (x86_64)
--
-- Host: localhost    Database: ovirt_development
-- ------------------------------------------------------
-- Server version	5.6.36

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
-- Table structure for table `assets`
--

DROP TABLE IF EXISTS `assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assets` (
  `CLIENT_MAC` varchar(255) NOT NULL DEFAULT '',
  `CLIENT_VNCPWD` varchar(255) DEFAULT NULL,
  `CLIENT_CFGPWD` varchar(255) DEFAULT NULL,
  `CLIENT_DFAPP` varchar(255) DEFAULT NULL,
  `CLIENT_DFSRV` varchar(255) DEFAULT NULL,
  `CLIENT_MEM` varchar(255) DEFAULT NULL,
  `CLIENT_GPU` varchar(255) DEFAULT NULL,
  `CLIENT_CPU` varchar(255) DEFAULT NULL,
  `CLIENT_NIC` varchar(255) DEFAULT NULL,
  `CLIENT_OS` varchar(255) DEFAULT NULL,
  `CLIENT_Model` varchar(255) DEFAULT NULL,
  `CLIENT_STORAGE` varchar(255) DEFAULT NULL,
  `CLIENT_KERNEL` varchar(255) DEFAULT NULL,
  `CLIENT_IP` varchar(255) DEFAULT NULL,
  `CLIENT_AUDIO` varchar(255) DEFAULT NULL,
  `CLIENT_VERSION` varchar(255) DEFAULT NULL,
  `CLIENT_NAME` varchar(255) DEFAULT NULL,
  `CLIENT_FREQ` varchar(255) DEFAULT NULL,
  `CLIENT_DISPLAY` varchar(255) DEFAULT NULL,
  `CLIENT_OPT` varchar(255) DEFAULT NULL,
  `CLIENT_SESSION_0_TYPE` varchar(255) DEFAULT NULL,
  `CLIENT_LANGUAGE` varchar(255) DEFAULT NULL,
  `CLIENT_GROUP` varchar(64) NOT NULL,
  PRIMARY KEY (`CLIENT_MAC`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assets`
--

LOCK TABLES `assets` WRITE;
/*!40000 ALTER TABLE `assets` DISABLE KEYS */;
INSERT INTO `assets` VALUES ('00301854C83D','12345678','','freerdp','172.16.128.11',' 1955632K',' Intel(R) HD Graphics',' Intel(R) Celeron(R) CPU  J1900  @ 1.99GHz',' Realtek Semiconductor Co., Ltd. RTL8111/8168B PCI Express Gigabit Ethernet controller (rev 07)',' Thinsys Linux',' Enterprise Edition','Disk /dev/sda: 8012 MB','Linux 3.14.13','172.16.128.65','  Intel Corporation Device 0f04 (rev 0e)','2012111580','TC004','DDRIII 1600Mhz init freq','1920x1080','sse2, sse3, ssse3, sse4.1, sse4.2','freerdp','zh_CN.utf8','class2');
/*!40000 ALTER TABLE `assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `groupmanage`
--

DROP TABLE IF EXISTS `groupmanage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groupmanage` (
  `GROUP_NAME` varchar(255) NOT NULL DEFAULT '',
  `GROUP_REMARK` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`GROUP_NAME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groupmanage`
--

LOCK TABLES `groupmanage` WRITE;
/*!40000 ALTER TABLE `groupmanage` DISABLE KEYS */;
INSERT INTO `groupmanage` VALUES ('class1','班级一'),('class2','班级二');
/*!40000 ALTER TABLE `groupmanage` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-10 17:40:10
