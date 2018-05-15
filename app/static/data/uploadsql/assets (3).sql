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
INSERT INTO `assets` VALUES ('0011180043C3','888888','','spice','172.16.129.228','1024MB RAM','Mali-400 MP4','ARM Cortex-A9 Quad-core 1.6GHz','10/100Mbps NIC','Thinsys Linux','Standard Edition','8GB Nand Flash','Linux 3.0.36+','172.16.129.50','alc5623 soc audio','2012111604','a01','DDRIII 1600Mhz init freq 456','1920x1080',' enabled VFP/NEON optimizations','spice','zh_CN.utf8','a1-12'),('0011180043CA','888888','','spice','172.16.129.228','1024MB RAM','Mali-400 MP4','ARM Cortex-A9 Quad-core 1.6GHz','10/100Mbps NIC','Thinsys Linux','Standard Edition','8GB Nand Flash','Linux 3.0.36+','172.16.129.70','alc5623 soc audio','2012111604','TC001','DDRIII 1600Mhz init freq 456','1920x1080',' enabled VFP/NEON optimizations','spice','zh_CN.utf8',''),('0011180043DD','888888','','spice','172.16.129.228','1024MB RAM','Mali-400 MP4','ARM Cortex-A9 Quad-core 1.6GHz','10/100Mbps NIC','Thinsys Linux','Standard Edition','8GB Nand Flash','Linux 3.0.36+','172.16.129.85','alc5623 soc audio','2012111604','a36','DDRIII 1600Mhz init freq 456','1920x1080',' enabled VFP/NEON optimizations','spice','zh_CN.utf8',''),('00301857D7EF','12345678','','spice','172.16.129.228',' 1953800K',' Intel(R) HD Graphics',' Intel(R) Celeron(R) CPU  N2805  @ 1.46GHz',' Realtek Semiconductor Co., Ltd. RTL8111/8168B PCI Express Gigabit Ethernet controller (rev 07)',' Thinsys Linux','Enterprise Edition','Disk /dev/sda: 8012 MB','Linux 3.14.13','172.16.129.56','  Intel Corporation Device 0f04 (rev 0a)','2012111581','x07','DDRIII 1600Mhz init freq','1024x768','sse2, sse3, ssse3, sse4.1, sse4.2','spice','zh_CN.utf8',''),('00301857D7F0','12345678','','spice','172.16.129.228',' 1953800K',' Intel(R) HD Graphics',' Intel(R) Celeron(R) CPU  N2805  @ 1.46GHz',' Realtek Semiconductor Co., Ltd. RTL8111/8168B PCI Express Gigabit Ethernet controller (rev 07)',' Thinsys Linux','Enterprise Edition','Disk /dev/sda: 8012 MB','Linux 3.14.13','172.16.129.50','  Intel Corporation Device 0f04 (rev 0a)','2012111581','x01','DDRIII 1600Mhz init freq','1024x768','sse2, sse3, ssse3, sse4.1, sse4.2','spice','zh_CN.utf8',''),('00301857D7F1','12345678','','spice','172.16.129.228',' 1953800K',' Intel(R) HD Graphics',' Intel(R) Celeron(R) CPU  N2805  @ 1.46GHz',' Realtek Semiconductor Co., Ltd. RTL8111/8168B PCI Express Gigabit Ethernet controller (rev 07)',' Thinsys Linux','Enterprise Edition','Disk /dev/sda: 8012 MB','Linux 3.14.13','172.16.129.51','  Intel Corporation Device 0f04 (rev 0a)','2012111581','x02','DDRIII 1600Mhz init freq','1440x900','sse2, sse3, ssse3, sse4.1, sse4.2','spice','zh_CN.utf8',''),('00301857D8A1','12345678','','spice','172.16.129.228',' 1953800K',' Intel(R) HD Graphics',' Intel(R) Celeron(R) CPU  N2805  @ 1.46GHz',' Realtek Semiconductor Co., Ltd. RTL8111/8168B PCI Express Gigabit Ethernet controller (rev 07)',' Thinsys Linux','Enterprise Edition','Disk /dev/sda: 8012 MB','Linux 3.14.13','172.16.129.55','  Intel Corporation Device 0f04 (rev 0a)','2012111581','x06','DDRIII 1600Mhz init freq','1024x768','sse2, sse3, ssse3, sse4.1, sse4.2','spice','zh_CN.utf8',''),('00301857D8AE','12345678','','spice','172.16.129.228',' 1953800K',' Intel(R) HD Graphics',' Intel(R) Celeron(R) CPU  N2805  @ 1.46GHz',' Realtek Semiconductor Co., Ltd. RTL8111/8168B PCI Express Gigabit Ethernet controller (rev 07)',' Thinsys Linux','Enterprise Edition','Disk /dev/sda: 8012 MB','Linux 3.14.13','172.16.129.52','  Intel Corporation Device 0f04 (rev 0a)','2012111581','x03','DDRIII 1600Mhz init freq','1024x768','sse2, sse3, ssse3, sse4.1, sse4.2','spice','zh_CN.utf8',''),('00301857D8E1','12345678','','spice','172.16.129.228',' 1953800K',' Intel(R) HD Graphics',' Intel(R) Celeron(R) CPU  N2805  @ 1.46GHz',' Realtek Semiconductor Co., Ltd. RTL8111/8168B PCI Express Gigabit Ethernet controller (rev 07)',' Thinsys Linux','Enterprise Edition','Disk /dev/sda: 8012 MB','Linux 3.14.13','172.16.129.58','  Intel Corporation Device 0f04 (rev 0a)','2012111581','x09','DDRIII 1600Mhz init freq','1024x768','sse2, sse3, ssse3, sse4.1, sse4.2','spice','zh_CN.utf8',''),('00301857F366','12345678','','spice','172.16.129.228',' 1953800K',' Intel(R) HD Graphics',' Intel(R) Celeron(R) CPU  N2805  @ 1.46GHz',' Realtek Semiconductor Co., Ltd. RTL8111/8168B PCI Express Gigabit Ethernet controller (rev 07)',' Thinsys Linux','Enterprise Edition','Disk /dev/sda: 8012 MB','Linux 3.14.13','172.16.129.53','  Intel Corporation Device 0f04 (rev 0a)','2012111581','x04','DDRIII 1600Mhz init freq','1024x768','sse2, sse3, ssse3, sse4.1, sse4.2','spice','zh_CN.utf8','');
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
INSERT INTO `groupmanage` VALUES ('a1-12',''),('a13-20',''),('a21-30',''),('a31-40','');
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

-- Dump completed on 2018-05-03 12:02:42
