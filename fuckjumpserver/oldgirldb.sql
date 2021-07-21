-- MySQL dump 10.13  Distrib 5.7.23, for Win64 (x86_64)
--
-- Host: localhost    Database: oldgirldb
-- ------------------------------------------------------
-- Server version	5.7.23

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
-- Table structure for table `audit_log`
--

DROP TABLE IF EXISTS `audit_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `audit_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `bind_host_id` int(11) DEFAULT NULL,
  `action_type` varchar(255) DEFAULT NULL,
  `cmd` varchar(255) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `bind_host_id` (`bind_host_id`),
  CONSTRAINT `audit_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_profile` (`id`),
  CONSTRAINT `audit_log_ibfk_2` FOREIGN KEY (`bind_host_id`) REFERENCES `bind_host` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_log`
--

LOCK TABLES `audit_log` WRITE;
/*!40000 ALTER TABLE `audit_log` DISABLE KEYS */;
INSERT INTO `audit_log` VALUES (1,2,1,'login',NULL,'2021-07-20 09:58:07'),(2,2,1,'cmd','ls','2021-07-20 09:58:13'),(3,2,1,'cmd','cd','2021-07-20 09:58:16'),(4,2,1,'cmd','ls','2021-07-20 10:18:37'),(5,2,1,'cmd','cd home','2021-07-20 10:18:44'),(6,2,1,'cmd','cd /home','2021-07-20 10:18:52'),(7,2,1,'cmd','cd jack','2021-07-20 10:18:53'),(8,2,1,'cmd','cd was','2021-07-20 10:18:56'),(9,2,1,'cmd','ls','2021-07-20 10:18:57'),(10,2,1,'cmd','cat demo.log','2021-07-20 10:19:05'),(11,2,1,'cmd','vim demo.txt','2021-07-20 10:19:43'),(12,2,1,'cmd',':q','2021-07-20 10:19:54'),(13,2,1,'cmd','ls','2021-07-20 10:20:01'),(14,2,1,'cmd','vim demo.log','2021-07-20 10:20:08'),(15,2,1,'cmd',':q','2021-07-20 10:20:20'),(16,2,1,'cmd','exit','2021-07-20 10:20:31'),(17,1,1,'login',NULL,'2021-07-20 11:21:01'),(18,1,1,'cmd','','2021-07-20 14:26:08'),(19,1,1,'cmd','exit','2021-07-20 14:26:09'),(20,1,1,'login',NULL,'2021-07-20 14:35:47'),(21,1,1,'cmd','exiy','2021-07-20 14:37:04'),(22,1,1,'cmd','exit','2021-07-20 14:37:06'),(23,1,1,'login',NULL,'2021-07-20 14:37:39'),(24,1,5,'login',NULL,'2021-07-20 15:01:41'),(25,1,5,'cmd','exit','2021-07-20 15:08:32'),(26,1,5,'login',NULL,'2021-07-20 15:09:16'),(27,1,5,'cmd','exit','2021-07-20 16:33:32'),(28,1,5,'login',NULL,'2021-07-20 16:34:19'),(29,1,5,'cmd','exit','2021-07-20 16:36:58'),(30,1,4,'login',NULL,'2021-07-20 16:42:04'),(31,1,4,'cmd','ls','2021-07-20 16:42:07'),(32,1,4,'cmd','mkdir jcm','2021-07-20 16:42:16'),(33,1,4,'cmd','cd jcm','2021-07-20 16:42:19'),(34,1,4,'cmd','ls','2021-07-20 16:42:20'),(35,1,4,'cmd','echo 123','2021-07-20 16:42:23'),(36,1,4,'cmd','exit','2021-07-20 16:51:38'),(37,2,4,'login',NULL,'2021-07-21 10:16:49'),(38,2,4,'cmd','ls','2021-07-21 10:17:59'),(39,2,4,'cmd','dir','2021-07-21 10:18:04'),(40,2,4,'cmd','exit','2021-07-21 10:23:57');
/*!40000 ALTER TABLE `audit_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bind_host`
--

DROP TABLE IF EXISTS `bind_host`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bind_host` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `host_id` int(11) DEFAULT NULL,
  `remoteuser_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_host_remoteuser_uc` (`host_id`,`remoteuser_id`),
  KEY `remoteuser_id` (`remoteuser_id`),
  CONSTRAINT `bind_host_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `host` (`id`),
  CONSTRAINT `bind_host_ibfk_2` FOREIGN KEY (`remoteuser_id`) REFERENCES `remote_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bind_host`
--

LOCK TABLES `bind_host` WRITE;
/*!40000 ALTER TABLE `bind_host` DISABLE KEYS */;
INSERT INTO `bind_host` VALUES (1,1,3),(5,2,1),(2,2,4),(4,2,5),(3,3,1);
/*!40000 ALTER TABLE `bind_host` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bindhost_m2m_hostgroup`
--

DROP TABLE IF EXISTS `bindhost_m2m_hostgroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bindhost_m2m_hostgroup` (
  `bindhost_id` int(11) DEFAULT NULL,
  `hostgroup_id` int(11) DEFAULT NULL,
  KEY `bindhost_id` (`bindhost_id`),
  KEY `hostgroup_id` (`hostgroup_id`),
  CONSTRAINT `bindhost_m2m_hostgroup_ibfk_1` FOREIGN KEY (`bindhost_id`) REFERENCES `bind_host` (`id`),
  CONSTRAINT `bindhost_m2m_hostgroup_ibfk_2` FOREIGN KEY (`hostgroup_id`) REFERENCES `host_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bindhost_m2m_hostgroup`
--

LOCK TABLES `bindhost_m2m_hostgroup` WRITE;
/*!40000 ALTER TABLE `bindhost_m2m_hostgroup` DISABLE KEYS */;
INSERT INTO `bindhost_m2m_hostgroup` VALUES (1,1),(2,1),(3,1),(3,2),(4,2),(5,2);
/*!40000 ALTER TABLE `bindhost_m2m_hostgroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `host`
--

DROP TABLE IF EXISTS `host`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(64) DEFAULT NULL,
  `ip` varchar(64) DEFAULT NULL,
  `port` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hostname` (`hostname`),
  UNIQUE KEY `ip` (`ip`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `host`
--

LOCK TABLES `host` WRITE;
/*!40000 ALTER TABLE `host` DISABLE KEYS */;
INSERT INTO `host` VALUES (1,'ubuntu test','192.168.190.131',22),(2,'server1','192.168.190.130',22),(3,'server2','10.4.4.22',22);
/*!40000 ALTER TABLE `host` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `host_group`
--

DROP TABLE IF EXISTS `host_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `host_group`
--

LOCK TABLES `host_group` WRITE;
/*!40000 ALTER TABLE `host_group` DISABLE KEYS */;
INSERT INTO `host_group` VALUES (1,'bj_group'),(2,'sh_group');
/*!40000 ALTER TABLE `host_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `remote_user`
--

DROP TABLE IF EXISTS `remote_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `remote_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `auth_type` varchar(255) DEFAULT NULL,
  `username` varchar(32) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_user_passwd_uc` (`auth_type`,`username`,`password`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `remote_user`
--

LOCK TABLES `remote_user` WRITE;
/*!40000 ALTER TABLE `remote_user` DISABLE KEYS */;
INSERT INTO `remote_user` VALUES (3,'ssh-key','root','123'),(4,'ssh-password','alex','alex3714'),(5,'ssh-password','mysql','123'),(1,'ssh-password','root','123'),(2,'ssh-password','root','alex!34321df');
/*!40000 ALTER TABLE `remote_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_m2m_bindhost`
--

DROP TABLE IF EXISTS `user_m2m_bindhost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_m2m_bindhost` (
  `userprofile_id` int(11) DEFAULT NULL,
  `bindhost_id` int(11) DEFAULT NULL,
  KEY `userprofile_id` (`userprofile_id`),
  KEY `bindhost_id` (`bindhost_id`),
  CONSTRAINT `user_m2m_bindhost_ibfk_1` FOREIGN KEY (`userprofile_id`) REFERENCES `user_profile` (`id`),
  CONSTRAINT `user_m2m_bindhost_ibfk_2` FOREIGN KEY (`bindhost_id`) REFERENCES `bind_host` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_m2m_bindhost`
--

LOCK TABLES `user_m2m_bindhost` WRITE;
/*!40000 ALTER TABLE `user_m2m_bindhost` DISABLE KEYS */;
INSERT INTO `user_m2m_bindhost` VALUES (2,1),(2,2),(5,3),(2,4),(1,5),(1,2),(1,4);
/*!40000 ALTER TABLE `user_m2m_bindhost` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_m2m_hostgroup`
--

DROP TABLE IF EXISTS `user_m2m_hostgroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_m2m_hostgroup` (
  `userprofile_id` int(11) DEFAULT NULL,
  `hostgroup_id` int(11) DEFAULT NULL,
  KEY `userprofile_id` (`userprofile_id`),
  KEY `hostgroup_id` (`hostgroup_id`),
  CONSTRAINT `user_m2m_hostgroup_ibfk_1` FOREIGN KEY (`userprofile_id`) REFERENCES `user_profile` (`id`),
  CONSTRAINT `user_m2m_hostgroup_ibfk_2` FOREIGN KEY (`hostgroup_id`) REFERENCES `host_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_m2m_hostgroup`
--

LOCK TABLES `user_m2m_hostgroup` WRITE;
/*!40000 ALTER TABLE `user_m2m_hostgroup` DISABLE KEYS */;
INSERT INTO `user_m2m_hostgroup` VALUES (2,1),(2,2),(1,1),(1,2);
/*!40000 ALTER TABLE `user_m2m_hostgroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_profile`
--

DROP TABLE IF EXISTS `user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(32) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_profile`
--

LOCK TABLES `user_profile` WRITE;
/*!40000 ALTER TABLE `user_profile` DISABLE KEYS */;
INSERT INTO `user_profile` VALUES (1,'alex','alex123'),(2,'jack','jack123'),(5,'rain','123');
/*!40000 ALTER TABLE `user_profile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-21 10:49:56
