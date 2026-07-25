-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: inclub_offline
-- ------------------------------------------------------
-- Server version	8.4.6

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cierres_caja`
--

DROP TABLE IF EXISTS `cierres_caja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cierres_caja` (
  `idcierre` int NOT NULL AUTO_INCREMENT,
  `idusuario` int NOT NULL,
  `idjornada` int NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `fecha_cierre` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idcierre`),
  KEY `idusuario` (`idusuario`),
  KEY `idjornada` (`idjornada`),
  CONSTRAINT `cierres_caja_ibfk_1` FOREIGN KEY (`idusuario`) REFERENCES `usuarios` (`idusuarios`),
  CONSTRAINT `cierres_caja_ibfk_2` FOREIGN KEY (`idjornada`) REFERENCES `jornadas` (`idjornada`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cierres_caja`
--

LOCK TABLES `cierres_caja` WRITE;
/*!40000 ALTER TABLE `cierres_caja` DISABLE KEYS */;
/*!40000 ALTER TABLE `cierres_caja` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente_puntos`
--

DROP TABLE IF EXISTS `cliente_puntos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente_puntos` (
  `idcliente` int NOT NULL,
  `puntos` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`idcliente`),
  CONSTRAINT `cliente_puntos_ibfk_1` FOREIGN KEY (`idcliente`) REFERENCES `clientes` (`idclientes`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente_puntos`
--

LOCK TABLES `cliente_puntos` WRITE;
/*!40000 ALTER TABLE `cliente_puntos` DISABLE KEYS */;
/*!40000 ALTER TABLE `cliente_puntos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `idclientes` int NOT NULL AUTO_INCREMENT,
  `apenomb` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `dni` int DEFAULT NULL,
  `cuil` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `correo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  PRIMARY KEY (`idclientes`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'CONSUMIDOR FINAL',0,'0','alguien@alguien.com','0001-01-01'),(5,'ALDERETE DYLAN EDUARDO',50008803,'20500088037','dalderete303@gmail.com','2000-02-10'),(6,'CARLOS MARTINEZ',544444,'2333232323','alguien@alguien.com','0001-01-01'),(7,'VALENTINA DE SANTIS',44446558,'0','VALENTINAESANTIS58@GMAIL.COM','2002-09-25');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes_puntos`
--

DROP TABLE IF EXISTS `clientes_puntos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes_puntos` (
  `idclientes` int NOT NULL,
  `puntos` int DEFAULT '0',
  PRIMARY KEY (`idclientes`),
  CONSTRAINT `clientes_puntos_ibfk_1` FOREIGN KEY (`idclientes`) REFERENCES `clientes` (`idclientes`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes_puntos`
--

LOCK TABLES `clientes_puntos` WRITE;
/*!40000 ALTER TABLE `clientes_puntos` DISABLE KEYS */;
/*!40000 ALTER TABLE `clientes_puntos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_entradas`
--

DROP TABLE IF EXISTS `detalle_entradas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_entradas` (
  `iddetalle` int NOT NULL AUTO_INCREMENT,
  `idventa` int NOT NULL,
  `idsector` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  PRIMARY KEY (`iddetalle`),
  KEY `idventa` (`idventa`),
  KEY `idsector` (`idsector`),
  CONSTRAINT `detalle_entradas_ibfk_1` FOREIGN KEY (`idventa`) REFERENCES `ventas_entradas` (`idventa`),
  CONSTRAINT `detalle_entradas_ibfk_2` FOREIGN KEY (`idsector`) REFERENCES `sectores` (`idsector`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_entradas`
--

LOCK TABLES `detalle_entradas` WRITE;
/*!40000 ALTER TABLE `detalle_entradas` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalle_entradas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jornadas`
--

DROP TABLE IF EXISTS `jornadas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jornadas` (
  `idjornada` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `clave` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `finicio` datetime DEFAULT NULL,
  `ffinal` datetime DEFAULT NULL,
  `estado` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'Activo',
  PRIMARY KEY (`idjornada`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jornadas`
--

LOCK TABLES `jornadas` WRITE;
/*!40000 ALTER TABLE `jornadas` DISABLE KEYS */;
INSERT INTO `jornadas` VALUES (1,'INCLUB','evento in','2026-01-12 00:00:00','2026-01-12 00:00:00','Finalizado'),(2,'PRUEBA2','inclub26','2026-01-11 00:00:00','2026-01-12 00:00:00','Finalizado'),(3,'BOLICHE','fescande','2026-01-10 00:00:00','2026-01-10 00:00:00','Finalizado'),(4,'BOLICHE','eventin','2026-01-09 00:00:00','2026-01-24 00:00:00','Finalizado'),(6,'EVENTO NAVIDEÑO','event in navidad','2026-01-23 00:00:00','2026-01-10 00:00:00','Finalizado'),(11,'FESTIMIEL','fest2026','2026-01-17 00:00:00','2026-01-18 00:00:00','Finalizado'),(12,'TOMORROW','tomo2026','2026-01-17 00:00:00','2026-01-18 00:00:00','Finalizado'),(13,'EVENTO DE PRUEBA','evenpru2026','2026-01-17 00:00:00','2026-01-18 00:00:00','Finalizado'),(14,'SAB 24 ENERO','1234','2026-01-24 00:00:00','2026-01-25 00:00:00','Finalizado'),(15,'PRUBA_CASA','prue','2026-01-24 00:00:00','2026-01-24 00:00:00','Finalizado'),(16,'SIMULARION ','1234','2026-01-31 00:00:00','2026-01-31 00:00:00','Finalizado'),(17,'ADMIN','1234','2026-01-28 00:00:00','2026-01-30 00:00:00','Finalizado'),(18,'PRUEBASSSSS','rrr','2026-01-29 00:00:00','2026-01-29 00:00:00','Finalizado'),(19,'CASA','1234','2026-01-29 00:00:00','2026-01-30 00:00:00','Finalizado'),(20,'METAN','1234','2026-02-01 00:00:00','2026-02-02 00:00:00','Activo');
/*!40000 ALTER TABLE `jornadas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jornadas_productos`
--

DROP TABLE IF EXISTS `jornadas_productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jornadas_productos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idjornada` int NOT NULL,
  `idproducto` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idjornada` (`idjornada`,`idproducto`),
  KEY `idproducto` (`idproducto`),
  CONSTRAINT `jornadas_productos_ibfk_1` FOREIGN KEY (`idjornada`) REFERENCES `jornadas` (`idjornada`),
  CONSTRAINT `jornadas_productos_ibfk_2` FOREIGN KEY (`idproducto`) REFERENCES `productos` (`idproductos`)
) ENGINE=InnoDB AUTO_INCREMENT=166 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jornadas_productos`
--

LOCK TABLES `jornadas_productos` WRITE;
/*!40000 ALTER TABLE `jornadas_productos` DISABLE KEYS */;
INSERT INTO `jornadas_productos` VALUES (1,11,2),(2,11,5),(3,11,6),(4,11,7),(5,11,8),(6,11,10),(7,11,16),(8,12,1),(18,12,2),(19,12,3),(9,12,4),(10,12,6),(20,12,7),(11,12,8),(12,12,9),(13,12,10),(21,12,12),(14,12,13),(15,12,14),(16,12,15),(17,12,17),(22,13,1),(23,13,2),(24,13,3),(25,13,4),(26,13,5),(27,13,6),(28,13,7),(29,13,8),(30,13,9),(31,13,10),(32,13,11),(33,13,12),(34,13,13),(35,13,14),(36,13,15),(37,13,16),(38,13,17),(39,13,18),(40,14,1),(41,14,2),(42,14,3),(43,14,4),(44,14,5),(45,14,6),(46,14,7),(47,14,8),(48,14,9),(49,14,10),(50,14,11),(51,14,12),(52,14,13),(53,14,14),(54,14,15),(55,14,16),(56,14,17),(57,14,18),(58,15,1),(59,15,2),(60,15,3),(61,15,4),(62,15,5),(63,15,6),(64,15,7),(65,15,8),(66,15,9),(67,15,10),(68,15,11),(69,15,12),(70,15,13),(71,15,14),(72,15,15),(73,15,16),(74,15,17),(75,15,18),(76,16,1),(77,16,2),(78,16,3),(79,16,4),(80,16,5),(81,16,6),(82,16,7),(83,16,8),(84,16,9),(85,16,10),(86,16,11),(87,16,12),(88,16,13),(89,16,14),(90,16,15),(91,16,16),(92,16,17),(93,16,18),(94,17,1),(95,17,2),(96,17,3),(97,17,4),(98,17,5),(99,17,6),(100,17,7),(101,17,8),(102,17,9),(103,17,10),(104,17,11),(105,17,12),(106,17,13),(107,17,14),(108,17,15),(109,17,16),(110,17,17),(111,17,18),(112,18,1),(113,18,2),(114,18,3),(115,18,4),(116,18,5),(117,18,6),(118,18,7),(119,18,8),(120,18,9),(121,18,10),(122,18,11),(123,18,12),(124,18,13),(125,18,14),(126,18,15),(127,18,16),(128,18,17),(129,18,18),(130,19,1),(131,19,2),(132,19,3),(133,19,4),(134,19,5),(135,19,6),(136,19,7),(137,19,8),(138,19,9),(139,19,10),(140,19,11),(141,19,12),(142,19,13),(143,19,14),(144,19,15),(145,19,16),(146,19,17),(147,19,18),(148,20,1),(149,20,2),(150,20,3),(151,20,4),(152,20,5),(153,20,6),(154,20,7),(155,20,8),(156,20,9),(157,20,10),(158,20,11),(159,20,12),(160,20,13),(161,20,14),(162,20,15),(163,20,16),(164,20,17),(165,20,18);
/*!40000 ALTER TABLE `jornadas_productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jornadas_puntos`
--

DROP TABLE IF EXISTS `jornadas_puntos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jornadas_puntos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idjornada` int NOT NULL,
  `idpunto` int NOT NULL,
  `estado` enum('Abierto','Cerrado') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'Abierto',
  `fecha_cierre` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idjornada` (`idjornada`,`idpunto`),
  KEY `idpunto` (`idpunto`),
  CONSTRAINT `jornadas_puntos_ibfk_1` FOREIGN KEY (`idjornada`) REFERENCES `jornadas` (`idjornada`),
  CONSTRAINT `jornadas_puntos_ibfk_2` FOREIGN KEY (`idpunto`) REFERENCES `puntos_venta` (`idpunto`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jornadas_puntos`
--

LOCK TABLES `jornadas_puntos` WRITE;
/*!40000 ALTER TABLE `jornadas_puntos` DISABLE KEYS */;
INSERT INTO `jornadas_puntos` VALUES (4,11,1,'Abierto',NULL),(5,11,6,'Abierto',NULL),(6,11,7,'Abierto',NULL),(7,12,1,'Abierto',NULL),(8,12,6,'Abierto',NULL),(9,12,7,'Abierto',NULL),(10,13,1,'Abierto',NULL),(11,13,6,'Abierto',NULL),(12,13,7,'Abierto',NULL),(13,14,1,'Abierto',NULL),(14,14,6,'Abierto',NULL),(15,14,7,'Abierto',NULL),(16,14,8,'Cerrado',NULL),(17,14,9,'Abierto',NULL),(18,14,10,'Abierto',NULL),(19,14,11,'Abierto',NULL),(20,15,1,'Abierto',NULL),(21,15,6,'Abierto',NULL),(22,15,7,'Abierto',NULL),(23,15,8,'Abierto',NULL),(24,15,9,'Abierto',NULL),(25,15,10,'Abierto',NULL),(26,15,11,'Abierto',NULL),(27,15,12,'Abierto',NULL),(28,15,13,'Abierto',NULL),(29,15,17,'Abierto',NULL),(30,15,18,'Abierto',NULL),(31,15,19,'Abierto',NULL),(32,16,1,'Abierto',NULL),(33,16,6,'Abierto',NULL),(34,16,7,'Abierto',NULL),(35,16,8,'Abierto',NULL),(36,16,9,'Abierto',NULL),(37,16,10,'Abierto',NULL),(38,16,11,'Abierto',NULL),(39,16,12,'Abierto',NULL),(40,16,13,'Abierto',NULL),(41,16,17,'Abierto',NULL),(42,16,18,'Abierto',NULL),(43,16,19,'Abierto',NULL),(44,17,19,'Abierto',NULL),(45,18,1,'Abierto',NULL),(46,18,6,'Abierto',NULL),(47,18,7,'Abierto',NULL),(48,18,8,'Abierto',NULL),(49,18,9,'Abierto',NULL),(50,18,10,'Abierto',NULL),(51,18,11,'Abierto',NULL),(52,18,12,'Abierto',NULL),(53,18,13,'Abierto',NULL),(54,18,17,'Abierto',NULL),(55,18,18,'Abierto',NULL),(56,18,19,'Abierto',NULL),(57,18,20,'Abierto',NULL),(58,19,1,'Abierto',NULL),(59,19,6,'Abierto',NULL),(60,19,7,'Abierto',NULL),(61,19,8,'Abierto',NULL),(62,19,9,'Abierto',NULL),(63,19,10,'Abierto',NULL),(64,19,11,'Abierto',NULL),(65,19,12,'Abierto',NULL),(66,19,13,'Abierto',NULL),(67,19,17,'Abierto',NULL),(68,19,18,'Abierto',NULL),(69,19,19,'Abierto',NULL),(70,19,20,'Abierto',NULL),(71,20,19,'Abierto',NULL),(72,20,20,'Abierto',NULL);
/*!40000 ALTER TABLE `jornadas_puntos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `modopago`
--

DROP TABLE IF EXISTS `modopago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `modopago` (
  `idmodopago` int NOT NULL AUTO_INCREMENT,
  `modo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `estado` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`idmodopago`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modopago`
--

LOCK TABLES `modopago` WRITE;
/*!40000 ALTER TABLE `modopago` DISABLE KEYS */;
INSERT INTO `modopago` VALUES (1,'EFECTIVO','Activo'),(2,'TRANSFERENCIA','Activo'),(3,'QR','Activo');
/*!40000 ALTER TABLE `modopago` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `precios_entradas`
--

DROP TABLE IF EXISTS `precios_entradas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `precios_entradas` (
  `idprecio` int NOT NULL AUTO_INCREMENT,
  `idjornada` int NOT NULL,
  `idsector` int NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `estado` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'Activo',
  PRIMARY KEY (`idprecio`),
  KEY `idjornada` (`idjornada`),
  KEY `idsector` (`idsector`),
  CONSTRAINT `precios_entradas_ibfk_1` FOREIGN KEY (`idjornada`) REFERENCES `jornadas` (`idjornada`),
  CONSTRAINT `precios_entradas_ibfk_2` FOREIGN KEY (`idsector`) REFERENCES `sectores` (`idsector`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `precios_entradas`
--

LOCK TABLES `precios_entradas` WRITE;
/*!40000 ALTER TABLE `precios_entradas` DISABLE KEYS */;
/*!40000 ALTER TABLE `precios_entradas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `idproductos` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `importe` double DEFAULT NULL,
  `estado` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `stock` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`idproductos`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,'ABSOLUT VODKAS',10000,'Activo',94),(2,'AGUA',5000,'Activo',84),(3,'CHANDON C/1 SPEED',37000,'Activo',0),(4,'CORONA',8000,'Activo',0),(5,'DR LEMON',7000,'Activo',0),(6,'FERNET',8000,'Activo',0),(7,'GANCIA',7000,'Activo',0),(8,'GIN',7000,'Activo',0),(9,'GASEOSA CHICA',5000,'Activo',0),(10,'HEINEKEN',7000,'Activo',0),(11,'HOLDMOSER',9000,'Activo',0),(12,'RENAIS C/ 1 SPEED',18000,'Activo',0),(13,'SMIRNOFF /SKK',9000,'Activo',0),(14,'SPEED',6000,'Activo',0),(15,'TRAGO COCTEL',8000,'Activo',0),(16,'VINO FINO',20000,'Activo',0),(17,'VODKA C/ SPEED',8000,'Activo',0),(18,'WHISKY HIRAM',12000,'Activo',0);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `puntos_beneficios`
--

DROP TABLE IF EXISTS `puntos_beneficios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `puntos_beneficios` (
  `idbeneficio` int NOT NULL AUTO_INCREMENT,
  `puntos_requeridos` int NOT NULL,
  `tipo` enum('CONSUMICION','DESCUENTO') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `valor` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`idbeneficio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `puntos_beneficios`
--

LOCK TABLES `puntos_beneficios` WRITE;
/*!40000 ALTER TABLE `puntos_beneficios` DISABLE KEYS */;
/*!40000 ALTER TABLE `puntos_beneficios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `puntos_venta`
--

DROP TABLE IF EXISTS `puntos_venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `puntos_venta` (
  `idpunto` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `idequipo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `estado` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`idpunto`),
  UNIQUE KEY `idequipo` (`idequipo`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `puntos_venta`
--

LOCK TABLES `puntos_venta` WRITE;
/*!40000 ALTER TABLE `puntos_venta` DISABLE KEYS */;
INSERT INTO `puntos_venta` VALUES (1,'CAJA10','192.168.100.92','Activo'),(6,'CAJA 9','192.168.100.89','Activo'),(7,'CAJA8','192.168.1.78','Activo'),(8,'CAJA12','192.168.1.89','Activo'),(9,'CAJA4','192.168.100.47','Activo'),(10,'CAJA3','192.168.100.138','Activo'),(11,'CAJA5','192.168.100.14','Activo'),(12,'CAJA6','192.168.100.177','Activo'),(13,'CAJA7','192.168.100.88','Activo'),(17,'CAJA8','192.168.100.95','Activo'),(18,'CAJA11','192.168.100.90','Activo'),(19,'INVITADO','192.168.1.106','Activo'),(20,'AUXILIAR','192.168.1.107','Activo');
/*!40000 ALTER TABLE `puntos_venta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sectores`
--

DROP TABLE IF EXISTS `sectores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sectores` (
  `idsector` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `estado` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'Activo',
  PRIMARY KEY (`idsector`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sectores`
--

LOCK TABLES `sectores` WRITE;
/*!40000 ALTER TABLE `sectores` DISABLE KEYS */;
/*!40000 ALTER TABLE `sectores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sectores_entradas`
--

DROP TABLE IF EXISTS `sectores_entradas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sectores_entradas` (
  `idsector` int NOT NULL AUTO_INCREMENT,
  `idjornada` int NOT NULL,
  `nombre` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `estado` enum('Activo','Inactivo') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'Activo',
  PRIMARY KEY (`idsector`),
  KEY `idjornada` (`idjornada`),
  CONSTRAINT `sectores_entradas_ibfk_1` FOREIGN KEY (`idjornada`) REFERENCES `jornadas` (`idjornada`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sectores_entradas`
--

LOCK TABLES `sectores_entradas` WRITE;
/*!40000 ALTER TABLE `sectores_entradas` DISABLE KEYS */;
INSERT INTO `sectores_entradas` VALUES (1,19,'GENERAL',10000.00,'Activo'),(2,13,'VIP',6000.00,'Activo'),(3,13,'Platea',4500.00,'Activo');
/*!40000 ALTER TABLE `sectores_entradas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `idusuarios` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `clave` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `rol` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `estado` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `operador` varchar(50) COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'OPERADOR',
  PRIMARY KEY (`idusuarios`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'ADMIN','123456','Administrador','Activo','OPERADOR'),(3,'CAJA9','1234','Vendedor','Activo','OPERADOR'),(4,'CAJA10','1234','Vendedor','Activo','OPERADOR'),(7,'CAJA12','1234','Vendedor','Activo','OPERADOR'),(8,'CAJA4','1234','Vendedor','Activo','OPERADOR'),(9,'CAJA3','1234','Vendedor','Activo','OPERADOR'),(10,'CAJA5','1234','Vendedor','Activo','OPERADOR'),(11,'CAJA6','1234','Vendedor','Activo','OPERADOR'),(12,'CAJA7','1234','Vendedor','Activo','OPERADOR'),(13,'CAJA8','1234','Vendedor','Activo','OPERADOR'),(14,'CAJA11','1234','Vendedor','Activo','OPERADOR'),(15,'INVITADO','1234','Vendedor','Activo','DIEGO ALDERETE'),(16,'AUX','1234','Vendedor','Activo','FENIX');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios_puntos`
--

DROP TABLE IF EXISTS `usuarios_puntos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios_puntos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idusuario` int NOT NULL,
  `idpunto` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idusuario` (`idusuario`,`idpunto`),
  KEY `idpunto` (`idpunto`),
  CONSTRAINT `usuarios_puntos_ibfk_1` FOREIGN KEY (`idusuario`) REFERENCES `usuarios` (`idusuarios`),
  CONSTRAINT `usuarios_puntos_ibfk_2` FOREIGN KEY (`idpunto`) REFERENCES `puntos_venta` (`idpunto`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios_puntos`
--

LOCK TABLES `usuarios_puntos` WRITE;
/*!40000 ALTER TABLE `usuarios_puntos` DISABLE KEYS */;
INSERT INTO `usuarios_puntos` VALUES (1,3,6),(11,4,1),(2,4,7),(9,4,17),(3,7,8),(4,8,9),(5,9,10),(6,10,11),(7,11,12),(8,12,13),(12,14,18),(13,15,19),(14,16,20);
/*!40000 ALTER TABLE `usuarios_puntos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas` (
  `idventa` int NOT NULL AUTO_INCREMENT,
  `idjornada` int NOT NULL,
  `idusuario` int NOT NULL,
  `idpunto` int NOT NULL,
  `idclientes` int DEFAULT NULL,
  `idmodopago` int DEFAULT NULL,
  `total` decimal(10,2) NOT NULL,
  `descuento_total` decimal(10,2) DEFAULT '0.00',
  `fecha_hora` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `estado` enum('PENDIENTE','OK','ANULADA') COLLATE utf8mb4_general_ci DEFAULT 'PENDIENTE',
  `observaciones` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `puntos_ganados` int DEFAULT '0',
  `qr_token` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `estado_ticket` enum('VALIDO','USADO','ANULADO') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'VALIDO',
  PRIMARY KEY (`idventa`),
  KEY `idjornada` (`idjornada`),
  KEY `idusuario` (`idusuario`),
  KEY `idpunto` (`idpunto`),
  KEY `idclientes` (`idclientes`),
  KEY `idmodopago` (`idmodopago`),
  CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`idjornada`) REFERENCES `jornadas` (`idjornada`),
  CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`idusuario`) REFERENCES `usuarios` (`idusuarios`),
  CONSTRAINT `ventas_ibfk_3` FOREIGN KEY (`idpunto`) REFERENCES `puntos_venta` (`idpunto`),
  CONSTRAINT `ventas_ibfk_4` FOREIGN KEY (`idclientes`) REFERENCES `clientes` (`idclientes`),
  CONSTRAINT `ventas_ibfk_5` FOREIGN KEY (`idmodopago`) REFERENCES `modopago` (`idmodopago`)
) ENGINE=InnoDB AUTO_INCREMENT=242 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (3,1,4,7,NULL,2,14000.00,0.00,'2026-01-11 14:55:09','OK','',140,'','VALIDO'),(4,1,4,7,NULL,2,25000.00,0.00,'2026-01-11 14:56:43','OK','',250,'','VALIDO'),(5,1,4,7,NULL,1,21000.00,0.00,'2026-01-11 14:59:10','OK','',140,'','VALIDO'),(6,1,4,7,1,2,14000.00,0.00,'2026-01-11 15:10:18','OK','',70,'','VALIDO'),(7,1,4,7,NULL,2,34000.00,0.00,'2026-01-11 16:37:49','OK','',340,'','VALIDO'),(8,1,4,7,NULL,2,28000.00,0.00,'2026-01-11 16:40:55','OK','',280,'','VALIDO'),(9,12,4,7,5,2,45000.00,0.00,'2026-01-12 14:32:49','OK','',450,'','VALIDO'),(10,12,3,6,NULL,2,10000.00,0.00,'2026-01-12 15:07:14','OK','',100,'','VALIDO'),(11,12,3,6,6,2,16000.00,0.00,'2026-01-12 15:08:16','OK','',160,'','VALIDO'),(12,12,3,6,NULL,2,7000.00,0.00,'2026-01-12 15:10:58','OK','',70,'','VALIDO'),(13,12,4,7,1,2,8000.00,0.00,'2026-01-12 15:41:08','OK','',80,'','VALIDO'),(14,12,4,7,1,2,8000.00,0.00,'2026-01-12 15:48:14','OK','',80,'','VALIDO'),(15,12,3,6,1,2,8000.00,0.00,'2026-01-12 15:49:04','OK','',80,'','VALIDO'),(16,12,4,7,1,2,14000.00,0.00,'2026-01-12 16:59:53','OK','',140,'','VALIDO'),(17,12,4,7,1,2,13000.00,0.00,'2026-01-12 17:03:35','OK','',130,'','VALIDO'),(18,12,4,7,1,2,13000.00,0.00,'2026-01-12 17:04:54','OK','',130,'','VALIDO'),(19,12,4,7,1,2,13000.00,0.00,'2026-01-12 17:06:07','OK','',130,'','VALIDO'),(20,12,4,7,1,2,18000.00,0.00,'2026-01-12 17:17:32','OK','',180,'','VALIDO'),(21,12,4,7,1,2,11000.00,0.00,'2026-01-12 17:24:43','OK','',110,'','VALIDO'),(22,12,4,7,5,2,14000.00,0.00,'2026-01-12 17:25:47','OK','',140,'','VALIDO'),(23,12,4,7,5,2,16000.00,0.00,'2026-01-12 22:22:12','OK','',160,'','VALIDO'),(24,12,4,7,6,2,37000.00,0.00,'2026-01-12 22:29:33','OK','',370,'','VALIDO'),(25,12,4,7,5,2,13000.00,0.00,'2026-01-12 22:46:49','OK','',130,'','VALIDO'),(26,12,4,7,5,2,12000.00,0.00,'2026-01-12 22:55:38','OK','',120,'','VALIDO'),(27,12,4,7,5,2,11000.00,0.00,'2026-01-12 22:56:36','OK','',110,'','VALIDO'),(28,12,4,7,6,2,12000.00,0.00,'2026-01-12 23:06:46','OK','',120,'','VALIDO'),(29,12,4,7,5,2,15000.00,0.00,'2026-01-12 23:21:06','OK','',150,'0aba1afea53e4d1993f7208e2131678b','VALIDO'),(30,12,4,7,1,2,7000.00,0.00,'2026-01-12 23:21:30','OK','',70,'1d57360b5d9447eab2df8013d289539c','VALIDO'),(31,12,4,7,1,2,15000.00,0.00,'2026-01-12 23:33:06','OK','',150,'1fff179d3c5240aab9ab67dc66cc1b3f','VALIDO'),(32,12,4,7,1,2,8000.00,0.00,'2026-01-13 21:14:27','OK','',80,'c9ec99e22c27430e8045905a715d053a','VALIDO'),(33,12,4,7,1,2,7000.00,0.00,'2026-01-13 21:15:56','OK','',70,'a2fea95aed304b6895d56f459686eaf1','VALIDO'),(34,12,4,7,1,2,16000.00,0.00,'2026-01-13 21:25:33','OK','',160,'b5e218485baf48f784aa2239345a83c1','VALIDO'),(35,12,4,7,5,2,13000.00,0.00,'2026-01-13 21:31:15','OK','',130,'47b24226b0f343209f936635a8d3cabf','VALIDO'),(36,12,4,7,1,2,14000.00,0.00,'2026-01-13 21:39:21','OK','',140,'9244e65e2cc14ed186ac7ade0611c217','VALIDO'),(37,12,4,7,1,2,37000.00,0.00,'2026-01-13 21:39:58','OK','',370,'af7ab040e96d4d1481194e12fb861692','VALIDO'),(38,12,4,7,6,2,23000.00,0.00,'2026-01-13 22:16:32','OK','',230,'a3200465e00944db82be76cd777b313c','VALIDO'),(39,12,4,7,1,2,8000.00,0.00,'2026-01-13 22:17:50','OK','',80,'6ee28f14dfe54291b0a7568ce06b84e9','VALIDO'),(40,12,4,7,1,2,8000.00,0.00,'2026-01-13 22:18:01','OK','',80,'f774aca922434c3f8765a32f1eab5c9a','VALIDO'),(41,12,4,7,1,2,8000.00,0.00,'2026-01-13 22:18:12','OK','',80,'ccecbf2b2079482a801a8d99d77a5f19','VALIDO'),(42,12,4,7,1,2,27000.00,0.00,'2026-01-13 22:25:53','OK','',270,'7e96108fb3e749ada000a96144be4e20','VALIDO'),(43,13,3,6,5,2,44000.00,0.00,'2026-01-15 07:50:29','OK','',440,'ecd7532b5ef540a9a5517da7d965fb68','VALIDO'),(44,13,3,6,1,2,19000.00,0.00,'2026-01-15 07:51:16','OK','',190,'b5da3c41c4904029826f820d3b1ef396','VALIDO'),(45,13,3,6,1,2,5000.00,0.00,'2026-01-15 07:54:08','OK','',50,'6b886cedb38140b59cc785e7058ddbfd','VALIDO'),(46,13,3,6,1,2,7000.00,0.00,'2026-01-15 08:49:12','OK','',70,'e134f4e7397e4271ad6b403ea95ed8db','VALIDO'),(47,13,4,7,1,2,19000.00,0.00,'2026-01-15 10:03:32','OK','',190,'b66f1ec9f30548e8a95b96a0f8ff8ef4','VALIDO'),(48,13,4,7,1,2,8000.00,0.00,'2026-01-15 10:03:49','OK','',80,'3e8e8208b4a343048206d4f7ff707b03','VALIDO'),(49,13,4,7,1,2,9000.00,0.00,'2026-01-15 10:04:03','OK','',90,'dd9512615e52402f81d08bad7353f85f','VALIDO'),(50,13,8,9,1,2,37000.00,0.00,'2026-01-16 18:43:26','OK','',370,'d36a8ec984ec4064ac9a59d8f5cd290c','VALIDO'),(51,13,8,9,1,2,14000.00,0.00,'2026-01-16 18:43:47','OK','',140,'405415cb78f74f4a8e2cb1e44e28a349','VALIDO'),(52,13,8,9,1,2,25000.00,0.00,'2026-01-16 18:47:41','OK','',250,'bae94d5985164e34ba0d09d87c0f9125','VALIDO'),(53,13,8,9,5,2,7000.00,0.00,'2026-01-16 18:48:45','OK','',70,'fbf4f3d13dab47c5bbdc41f8b3082bf0','VALIDO'),(54,13,9,10,1,2,7000.00,0.00,'2026-01-16 18:56:03','OK','',70,'1468f7951bb34d6dad559270a7dc374d','VALIDO'),(55,13,9,10,1,2,7000.00,0.00,'2026-01-16 18:56:25','OK','',70,'7fc71d815abd497f97144f1cd3328b7d','VALIDO'),(56,13,10,11,1,2,7000.00,0.00,'2026-01-16 19:02:14','OK','',70,'cb54618b773e4d1c894479e0711a3ff1','VALIDO'),(57,13,10,11,1,2,8000.00,0.00,'2026-01-16 19:02:48','OK','',80,'bc40b0d18364487bb127c441df0eda19','VALIDO'),(58,13,10,11,1,2,18000.00,0.00,'2026-01-16 19:05:36','OK','',180,'b75770680f0745c78a5e60bc3e532f95','VALIDO'),(59,13,10,11,5,1,5000.00,0.00,'2026-01-20 16:25:32','OK','',50,'e805542c5ea1401fbcb11c288365067c','VALIDO'),(60,13,10,11,7,2,37000.00,0.00,'2026-01-20 16:28:29','OK','',370,'9fec08f28af14196acebcf8b02a1c4a0','VALIDO'),(61,13,9,10,6,2,10000.00,0.00,'2026-01-20 16:29:04','OK','',100,'f9e8baf69a1e484b9729fb5b7bbf8cba','VALIDO'),(62,13,10,11,1,2,0.00,0.00,'2026-01-20 16:29:55','OK','',0,'e63a217e1bf84e59b58864ba9699bace','VALIDO'),(63,13,10,11,7,2,16000.00,0.00,'2026-01-20 16:31:03','OK','',160,'688bef947cd74fd1b35c634c94f3f72d','VALIDO'),(64,13,10,11,1,2,40000.00,0.00,'2026-01-20 16:33:21','OK','',400,'f47cb5e9a0fb4f148c7ae9859bc45911','VALIDO'),(65,14,10,11,7,2,37000.00,0.00,'2026-01-20 16:43:39','OK','',370,'96d080edd1924176a7baaf9f9e949cbf','VALIDO'),(66,14,14,18,1,2,8000.00,0.00,'2026-01-20 18:04:35','OK','',80,'e4ceca8c58024ef488659f83db8aabba','VALIDO'),(67,14,14,18,1,2,7000.00,0.00,'2026-01-20 18:05:07','OK','',70,'9d9873c6e6ea421090f982e4460f928f','VALIDO'),(68,14,14,18,1,2,7000.00,0.00,'2026-01-20 18:05:45','OK','',70,'d4ee0ae0c7704ab08b14b4558cc61bcb','VALIDO'),(69,14,10,11,1,2,7000.00,0.00,'2026-01-20 18:09:06','OK','',70,'42f141bde1d44389a9e2ed41037080bf','VALIDO'),(70,14,14,18,1,2,7000.00,0.00,'2026-01-20 18:19:21','OK','',70,'783278c074a44d8f85f97917c4bd7fb8','VALIDO'),(71,14,14,18,1,2,7000.00,0.00,'2026-01-20 18:19:45','OK','',70,'3389d0a452f74faf89f84ee83dfc7f6c','VALIDO'),(72,14,10,11,1,2,7000.00,0.00,'2026-01-20 18:21:21','OK','',70,'4f95108a9e284d2c92d1e6d46dfa516a','VALIDO'),(73,14,10,11,1,2,7000.00,0.00,'2026-01-20 18:23:31','OK','',70,'00b689e06a80461e8c660f92fcf2ad15','VALIDO'),(74,14,10,11,1,2,18000.00,0.00,'2026-01-20 18:23:47','OK','',180,'4dbd28a36e1a40dfa0acb2c20f240971','VALIDO'),(75,14,14,18,1,2,9000.00,0.00,'2026-01-20 18:28:16','OK','',90,'cf3ffc52a82a4115b70eb46d9e34193f','VALIDO'),(76,14,14,18,1,2,10000.00,0.00,'2026-01-20 18:31:56','OK','',100,'9f064eba8eed44d2bb7bea69e2496c1d','VALIDO'),(77,14,14,18,1,2,37000.00,0.00,'2026-01-20 18:33:49','OK','',370,'f50bd27154e844a794464ef3ec14bbf1','VALIDO'),(78,14,10,11,1,2,18000.00,0.00,'2026-01-20 18:38:02','OK','',180,'bcfe202af4e245f6bdb8bd1b92b96eb6','VALIDO'),(79,14,14,18,1,2,18000.00,0.00,'2026-01-20 18:38:49','OK','',180,'663d671958b34ab69d38368975ca64ca','VALIDO'),(80,14,3,6,1,2,9000.00,0.00,'2026-01-20 18:51:46','OK','',90,'19124cf8415b48be9416443f0e78f186','VALIDO'),(81,14,4,1,1,2,9000.00,0.00,'2026-01-20 18:55:28','OK','',90,'e933253394d642149099f96296a6733e','VALIDO'),(82,14,11,12,1,2,14000.00,0.00,'2026-01-20 18:57:33','OK','',140,'681d6110206b48609d78b921572b69a4','VALIDO'),(83,14,11,12,1,2,26000.00,0.00,'2026-01-20 19:00:01','OK','',260,'3fcef1b1e90446eb9bea5f7ae2f220dd','VALIDO'),(84,14,11,12,1,2,15000.00,0.00,'2026-01-20 19:02:37','OK','',150,'ef3557e8521544a2ade0ad4a90a510c6','VALIDO'),(85,14,3,6,1,2,14000.00,0.00,'2026-01-20 19:04:49','OK','',140,'f32d6d0d73f54cd8b9fac4637989e142','VALIDO'),(86,14,3,6,1,2,21000.00,0.00,'2026-01-20 19:05:05','OK','',210,'a17cc6566d384644af1ed0b68faf49ad','VALIDO'),(87,14,4,1,1,2,17000.00,0.00,'2026-01-20 19:09:01','OK','',170,'b05fa0e9a54d4d889c2af4251350e81f','VALIDO'),(88,14,4,17,1,2,12000.00,0.00,'2026-01-20 19:11:19','OK','',120,'381a8d388c1c4133933a2246d041ed23','VALIDO'),(89,14,12,13,1,2,15000.00,0.00,'2026-01-20 19:16:37','OK','',150,'a3fa19cd64e24e2496b955f53e6e37c5','VALIDO'),(90,14,7,8,1,2,27000.00,0.00,'2026-01-21 08:13:30','OK','',270,'4328a6dbef6d4d93befbe14da576c361','VALIDO'),(91,14,7,8,1,2,8000.00,0.00,'2026-01-21 12:14:14','OK','',80,'d22bec88493d49ae8ed6820400d5d3e0','VALIDO'),(92,14,7,8,1,2,9000.00,0.00,'2026-01-21 12:36:44','OK','',90,'dc6a1fd65656454c9552dbfcb125293a','VALIDO'),(93,14,7,8,1,2,6000.00,0.00,'2026-01-21 12:37:59','OK','',60,'9edf3b5eacd845c6bda1d36175d5ec3e','VALIDO'),(94,14,7,8,1,2,13000.00,0.00,'2026-01-21 13:27:14','OK','',130,'09c1768df81f4ffa945f0eea3a475d15','VALIDO'),(95,14,7,8,1,2,14000.00,0.00,'2026-01-23 15:43:37','OK','',140,'06aaebc4f2e64792b1252dde39d941bd','VALIDO'),(96,14,7,8,1,1,8000.00,0.00,'2026-01-23 16:15:39','OK','',80,'fad818520190408387335dcac6951134','VALIDO'),(97,14,7,8,5,1,7000.00,0.00,'2026-01-23 16:16:05','OK','',70,'ab8a5dd19c544ccb8ff27d89805f5b96','VALIDO'),(98,14,7,8,6,1,7000.00,0.00,'2026-01-23 16:21:51','OK','',70,'13f8cfe83a4f48f786b60365f616a600','VALIDO'),(99,14,7,8,1,1,5000.00,0.00,'2026-01-23 16:27:35','OK','',50,'0c73c70e5bf24818ba7126490bd098f6','VALIDO'),(100,14,7,8,1,2,0.00,0.00,'2026-01-23 17:16:18','OK','',0,'70253bf84d5f4a04b7a0efa05be56c66','VALIDO'),(101,14,7,8,1,2,0.00,0.00,'2026-01-23 17:20:58','OK','',0,'8d566f68d5aa4a46bf4b09944d6d2df9','VALIDO'),(102,14,7,8,1,2,0.00,0.00,'2026-01-23 17:24:17','OK','',0,'ad2c8893241d472fb2f763a7b322ba0c','VALIDO'),(103,14,7,8,1,2,0.00,0.00,'2026-01-23 17:25:56','OK','',0,'f3149e1aa47c43a5954839598acad25c','VALIDO'),(104,14,7,8,1,1,7000.00,0.00,'2026-01-23 17:30:59','OK','',70,'319dd15cf531499386c070091bcc9ce8','VALIDO'),(105,14,7,8,1,2,8000.00,0.00,'2026-01-23 17:31:38','OK','',80,'f94ad7455b654594b5bd54b44a218dab','VALIDO'),(106,14,7,8,1,2,8000.00,0.00,'2026-01-23 17:36:49','OK','',80,'d7a9e31114c74821bab75056cfe9b701','VALIDO'),(107,14,7,8,1,2,7000.00,0.00,'2026-01-23 17:40:33','OK','',70,'f03bcb1ea4d44434926c9cf57b6cb3a9','VALIDO'),(108,14,7,8,1,2,8000.00,0.00,'2026-01-23 17:43:15','OK','',80,'46e3ff7466d4443facc3b4ee9a7b724f','VALIDO'),(109,14,7,8,1,2,7000.00,0.00,'2026-01-23 17:44:48','OK','',70,'66dc66e905f3435ab043a22e2608d1d3','VALIDO'),(110,14,7,8,1,2,7000.00,0.00,'2026-01-23 17:48:03','OK','',70,'474000d4a30449ff82babe5dd1944907','VALIDO'),(111,14,7,8,1,2,7000.00,0.00,'2026-01-23 17:52:25','OK','',70,'413eab443a3147a0a1601ec7505dbb5f','VALIDO'),(112,14,7,8,1,2,20000.00,0.00,'2026-01-23 17:56:21','OK','',200,'4ef5bfc2103341f59648770d31dada2f','VALIDO'),(113,14,7,8,1,2,0.00,0.00,'2026-01-23 17:58:26','OK','',0,'0670d1a926204b49bfafb5979779e8fa','VALIDO'),(114,14,7,8,1,1,7000.00,0.00,'2026-01-23 18:27:13','OK','',70,'f89585bdc5a147e68b0c0c004e77cba8','VALIDO'),(115,14,7,8,1,2,0.00,0.00,'2026-01-23 18:27:39','OK','',0,'36ed0722b46340abafe68cf13527eaf9','VALIDO'),(116,14,7,8,1,2,8000.00,0.00,'2026-01-23 18:27:59','OK','',80,'8b334f935f134836a333511d51fe3d21','VALIDO'),(117,14,7,8,1,2,5000.00,0.00,'2026-01-23 18:36:38','OK','',50,'2e977f05276e4b12ab20fc3e71035174','VALIDO'),(118,14,7,8,1,2,9000.00,0.00,'2026-01-23 18:37:50','OK','',90,'0eea7be137ab46ae8311063b580c693c','VALIDO'),(120,15,15,19,1,2,7000.00,0.00,'2026-01-24 07:52:28','OK','',70,'56cc98f400864a9f841915b472b131cb','VALIDO'),(121,15,15,19,1,2,20000.00,0.00,'2026-01-24 07:52:52','OK','',200,'4df49e80a7c141029a8e112777933ec1','VALIDO'),(122,15,15,19,1,1,7000.00,0.00,'2026-01-24 07:55:54','OK','',70,'c311c2d76b384f13a85bd427011eeb50','VALIDO'),(123,15,15,19,1,2,8000.00,0.00,'2026-01-24 07:56:03','OK','',80,'992b07dfb7f9421483b7aeed496b19ad','VALIDO'),(124,15,15,19,6,1,26000.00,0.00,'2026-01-24 07:56:30','OK','',260,'bae045936f0847c88f08ae4608a4e0f6','VALIDO'),(125,15,15,19,1,1,5000.00,0.00,'2026-01-24 09:44:58','OK','',50,'f50fbddc657243d98caf037b291a8b94','VALIDO'),(126,15,15,19,1,1,20000.00,0.00,'2026-01-24 09:48:39','OK','',200,'41b77bb39ed24df4979e6a5a4f53d4e4','VALIDO'),(127,15,15,19,1,1,6000.00,0.00,'2026-01-24 09:56:14','OK','',60,'4f8a3c8da37746a3a5d4179163aaae54','VALIDO'),(128,15,15,19,1,1,8000.00,0.00,'2026-01-24 09:57:41','OK','',80,'c9d7f55a72704ba7b2cfcdd9fb50bfaf','VALIDO'),(129,15,15,19,1,2,20000.00,0.00,'2026-01-24 10:00:42','OK','',200,'66e069ce1d7b49a4831b024da6f2741b','VALIDO'),(130,15,15,19,1,2,8000.00,0.00,'2026-01-24 10:01:41','OK','',80,'99b40c4f237d4879a58a70974994f6ac','VALIDO'),(131,15,15,19,1,2,6000.00,0.00,'2026-01-24 10:02:51','OK','',60,'3352a83109ea471c8c7cc5ee1f0ba072','VALIDO'),(132,15,15,19,1,2,18000.00,0.00,'2026-01-24 10:04:10','OK','',180,'d29ce02c6f2b4e87b6a42c712ec29a13','VALIDO'),(133,15,15,19,1,1,20000.00,0.00,'2026-01-24 11:12:26','OK','',200,'fb434924a8394824ab4dcd950875a766','VALIDO'),(134,15,15,19,1,2,8000.00,0.00,'2026-01-24 12:05:21','OK','',80,'8e6c43e284b640cca5d3f4ec60536f38','VALIDO'),(135,15,15,19,1,3,14000.00,0.00,'2026-01-24 12:11:37','OK','',140,'d5b7f68a72374fd292c1dd5482810898','VALIDO'),(136,15,15,19,5,3,12000.00,0.00,'2026-01-24 12:19:39','OK','',120,'b2fdb39bb67c4bee8e20f07f0e6f9f81','VALIDO'),(137,15,15,19,1,3,14000.00,0.00,'2026-01-24 12:20:39','OK','',140,'5e2a013647834a6283f3a88a368c0386','VALIDO'),(138,15,15,19,5,3,15000.00,0.00,'2026-01-24 12:32:07','OK','',150,'dd9b3ca2b68441028b78e593f505b269','VALIDO'),(139,15,15,19,1,3,17000.00,0.00,'2026-01-24 12:32:47','OK','',170,'1c19596ffb334801944558c0ee3eb4fa','VALIDO'),(140,15,15,19,1,1,20000.00,0.00,'2026-01-24 12:36:36','OK','',200,'0514ffb994f04d7cb33270efdd11f5f8','VALIDO'),(141,15,15,19,1,1,8000.00,0.00,'2026-01-24 12:37:49','OK','',80,'f26aaaf966214e13a818b89bd2d472e0','VALIDO'),(142,15,15,19,1,1,5000.00,0.00,'2026-01-24 12:38:00','OK','',50,'2530d66203a043df99e601eb79edf026','VALIDO'),(143,15,15,19,5,3,14000.00,0.00,'2026-01-24 12:38:48','OK','',140,'7519fee5898e4320931ed39f85d3ba12','VALIDO'),(144,15,15,19,1,1,8000.00,0.00,'2026-01-24 13:39:02','OK','',80,'a763b78752a3446ba3c58692b7afd749','VALIDO'),(145,15,15,19,1,3,20000.00,0.00,'2026-01-24 13:39:57','OK','',200,'a823cfc52fcb4814841ef83e70c8c521','VALIDO'),(146,15,15,19,1,3,20000.00,0.00,'2026-01-24 13:41:15','OK','',200,'60501042aa554839a4049b15e6189a34','VALIDO'),(147,15,15,19,1,3,17000.00,0.00,'2026-01-24 13:47:34','OK','',170,'770b1d6066d542cd8a268840aef14f82','VALIDO'),(148,15,15,19,1,1,8000.00,0.00,'2026-01-24 13:49:44','OK','',80,'a49a2eac2f764989a74ffe579c125a3e','VALIDO'),(149,15,15,19,1,1,7000.00,0.00,'2026-01-24 14:05:31','OK','',70,'d2447c311b314c7aa06c2ab7b4a7e373','VALIDO'),(150,15,15,19,1,1,26000.00,0.00,'2026-01-24 14:06:13','OK','',260,'c30044641e9e47dc82a7a125bd7e2b8d','VALIDO'),(151,15,15,19,1,1,8000.00,0.00,'2026-01-24 14:09:25','OK','',80,'e5aa44f7d25d459faf2c7c814e9624c2','VALIDO'),(152,15,15,19,1,3,12000.00,0.00,'2026-01-24 14:10:02','OK','',120,'e52a84274e6947b999449ad2b3d0a535','VALIDO'),(153,15,15,19,1,1,8000.00,0.00,'2026-01-24 14:14:57','OK','',80,'d2f7a5076e894ad49c5f52644a28c563','VALIDO'),(154,15,15,19,1,3,17000.00,0.00,'2026-01-24 14:15:35','OK','',170,'2650d4524b7f443aa62707d23ad04855','VALIDO'),(155,15,15,19,1,3,26000.00,0.00,'2026-01-24 14:19:11','OK','',260,'042c30cdb9a84dfbbfcd488acad8f56b','VALIDO'),(156,15,15,19,5,3,28000.00,0.00,'2026-01-24 14:25:35','OK','',280,'48d2d34ce44741a594e4c83097ee1b93','VALIDO'),(157,15,15,19,1,3,15000.00,0.00,'2026-01-24 14:28:20','OK','',150,'df14651992eb47038221bd5a100eda30','VALIDO'),(158,15,15,19,1,3,9000.00,0.00,'2026-01-24 14:33:32','OK','',90,'6e4dc082ca48479d9dd33cede23a9e87','VALIDO'),(159,15,15,19,1,3,9000.00,0.00,'2026-01-24 14:34:25','OK','',90,'479a72e9280d4a928cf6f7fc09a487f8','VALIDO'),(160,15,15,19,1,1,20000.00,0.00,'2026-01-24 14:35:02','OK','',200,'da286b536f53417da0b23bac8c51e0d5','VALIDO'),(161,15,15,19,1,1,8000.00,0.00,'2026-01-24 15:17:43','OK','',80,'935dfe7340174b08b4433dc4086a9d51','VALIDO'),(162,15,15,19,1,1,8000.00,0.00,'2026-01-24 15:21:42','OK','',80,'962a987bca4342b6a490ab24c38ae360','VALIDO'),(163,15,15,19,1,3,15000.00,0.00,'2026-01-24 16:33:16','OK','',150,'52d2fb61a6df4a07bdbb2bc4cc2b9e9c','VALIDO'),(164,15,15,19,1,1,8000.00,0.00,'2026-01-26 14:16:09','OK','',80,'5a520a9bce5545a1951d3ace835bb11a','VALIDO'),(165,15,15,19,1,NULL,15000.00,0.00,'2026-01-26 14:20:34','OK','',150,'9ccf74999ee641b5a5a28668bbc26cd8','VALIDO'),(166,15,15,19,1,1,7000.00,0.00,'2026-01-26 14:21:22','OK','',70,'f1a87367b9c94e2eaaea38808d63e810','VALIDO'),(167,15,15,19,1,2,8000.00,0.00,'2026-01-26 14:21:36','OK','',80,'33f8d163ac124d70ba969a01b454a2e3','VALIDO'),(168,15,15,19,1,NULL,8000.00,0.00,'2026-01-26 14:27:19','OK','',80,'373385ad43e445f7ba602afb20aa61a6','VALIDO'),(169,16,15,19,1,1,7000.00,0.00,'2026-01-26 14:39:41','OK','',70,'11b967d68e814a84aeb4c29531319c0e','VALIDO'),(170,16,15,19,1,2,20000.00,0.00,'2026-01-26 14:40:06','OK','',200,'4687279147cb4e1ebb620fb3c27846f4','VALIDO'),(171,16,15,19,1,1,8000.00,0.00,'2026-01-26 14:41:23','OK','',80,'081ad7087407483ead502702155adaa0','VALIDO'),(172,16,15,19,1,NULL,7000.00,0.00,'2026-01-26 14:42:12','OK','',70,'d3078fdcd4664b83b6d3cd48d62c9704','VALIDO'),(173,16,15,19,1,1,0.00,0.00,'2026-01-26 14:46:15','OK','',0,'d4512f710b5b436cafa3fd7cd2b01613','VALIDO'),(174,16,15,19,1,1,7000.00,0.00,'2026-01-26 15:00:05','OK','',70,'cf1d911072424bae9d863a6864a43aff','VALIDO'),(175,16,15,19,1,1,5000.00,0.00,'2026-01-26 15:02:43','OK','',50,'788a96d212904befb9b1b0124f2edcc4','VALIDO'),(176,16,15,19,1,NULL,20000.00,0.00,'2026-01-26 15:03:33','OK','',200,'c99b1f1b4961491bbc1a008d2aa4e7d1','VALIDO'),(177,17,15,19,1,NULL,8000.00,0.00,'2026-01-26 15:05:49','OK','',80,'e991736634c6488f9b8cbbabae7cfbbd','VALIDO'),(178,17,15,19,1,1,5000.00,0.00,'2026-01-26 15:06:54','OK','',50,'e579ce4f01af49a7ae6c81c5969ca369','VALIDO'),(179,17,15,19,1,1,0.00,0.00,'2026-01-26 15:16:32','OK','',0,'36419e16af654b5ca93dc9e5bebae99b','VALIDO'),(180,17,15,19,1,1,0.00,0.00,'2026-01-26 15:34:01','OK','',0,'d3d58f4fc39a4e0d8b4b07783030f232','VALIDO'),(181,17,15,19,1,1,7000.00,0.00,'2026-01-26 15:34:22','OK','',70,'62052e368d1949e99a050ad47176a459','VALIDO'),(182,17,15,19,1,NULL,8000.00,0.00,'2026-01-26 15:35:00','OK','',80,'26495846cc9c42d0abc273761e968db1','VALIDO'),(183,17,15,19,1,1,33000.00,0.00,'2026-01-26 17:48:24','OK','',330,'cffe6e619b6541b998de44d14cc4b7c2','VALIDO'),(184,18,15,19,1,1,18000.00,0.00,'2026-01-28 22:42:01','OK','',180,'f2474145d995412c964074f683919938','VALIDO'),(185,18,15,19,1,1,6000.00,0.00,'2026-01-28 23:22:56','OK','',60,'88452cda0c8f4f7ca99164ef5da8d92e','VALIDO'),(186,18,15,19,1,NULL,18000.00,0.00,'2026-01-28 23:23:54','OK','',180,'7e73e5b288ff48729ad00f3955e40953','VALIDO'),(187,18,15,19,1,1,8000.00,0.00,'2026-01-28 23:30:44','OK','',80,'c017f21b8ebe43a391f8ae78b923509f','VALIDO'),(188,18,15,19,1,1,7000.00,0.00,'2026-01-28 23:31:13','OK','',70,'fec7c9b95938479b81900a5a8cd45bcc','VALIDO'),(189,18,15,19,1,1,46000.00,0.00,'2026-01-28 23:31:39','OK','',460,'2cd4b18e22084b5091285f8c1cb78096','VALIDO'),(190,18,15,19,1,1,19000.00,0.00,'2026-01-28 23:32:19','OK','',190,'a24c7fc606274635b9c5053ea83aa258','VALIDO'),(191,18,15,19,1,NULL,18000.00,0.00,'2026-01-28 23:32:57','OK','',180,'66382bd8630148d9ae60760c6d3076c8','VALIDO'),(192,18,15,19,1,1,0.00,0.00,'2026-01-28 23:33:24','OK','',0,'c65f287226424153998213452b317f44','VALIDO'),(193,18,15,19,1,1,7000.00,0.00,'2026-01-28 23:35:11','OK','',70,'244035dccaf84de8bfd2645d048c1b53','VALIDO'),(194,18,15,19,5,1,9000.00,0.00,'2026-01-28 23:35:48','OK','',90,'d5444da6847047c191431655d6ac83c3','VALIDO'),(196,19,15,19,1,1,5000.00,0.00,'2026-01-29 23:55:28','OK','',50,'418f7d81ca224faaa617033fd02cf15c','VALIDO'),(197,19,15,19,1,1,7000.00,0.00,'2026-01-30 00:08:18','OK','',70,'48940e0904934ba98bdad9f2e0f84d28','VALIDO'),(204,19,15,19,1,1,5000.00,0.00,'2026-01-30 00:26:26','OK','',50,'a748cedd467a495eb218e7fcfe79d4ec','VALIDO'),(205,19,15,19,1,1,7000.00,0.00,'2026-01-30 00:29:40','OK','',70,'93c270f52518435a9cf639431b1f6e96','VALIDO'),(206,19,15,19,1,1,7000.00,0.00,'2026-01-30 00:29:49','OK','',70,'17b12467426e454290de43bcdbd7dfbb','VALIDO'),(207,19,15,19,1,1,7000.00,0.00,'2026-01-30 00:33:46','OK','',70,'bfa1d00d82074b118c36d08c461d8352','VALIDO'),(208,19,15,19,1,1,7000.00,0.00,'2026-01-30 00:35:40','OK','',70,'9bf3ac4e630a41d18c053230ad54e168','VALIDO'),(209,19,15,19,1,1,5000.00,0.00,'2026-01-30 00:35:59','OK','',50,'b57055ccaab64bd18ecf1f16100d8232','VALIDO'),(210,19,15,19,1,1,7000.00,0.00,'2026-01-30 00:41:45','OK','',70,'cf50784f8950445d8be9bb36c5c25360','VALIDO'),(211,19,15,19,1,1,5000.00,0.00,'2026-01-30 00:46:47','OK','',50,'848ab0d7541e43b58b35024611ff1091','VALIDO'),(212,19,15,19,1,1,10000.00,0.00,'2026-01-30 00:50:28','OK','',100,'79c2d987eabd4b1fbd9e8486a6c7d47c','VALIDO'),(213,19,15,19,1,1,10000.00,0.00,'2026-01-30 00:50:41','OK','',100,'76791a81e21f42a1b2e79ab81ae5bcec','VALIDO'),(214,19,15,19,1,1,5000.00,0.00,'2026-01-30 00:53:08','OK','',50,'0ccdca0c05c141bcaef697d9a13c754a','VALIDO'),(215,19,15,19,1,1,7000.00,0.00,'2026-01-30 00:53:18','OK','',70,'f533ceb10be045e39a0c22867222f85f','VALIDO'),(216,19,15,19,1,1,7000.00,0.00,'2026-01-30 00:53:26','OK','',70,'07cc3c6961c74335bd6577c78b00dfc1','VALIDO'),(217,19,15,19,1,NULL,5000.00,0.00,'2026-01-30 00:57:10','OK','',50,'56bd5be6bc914e089171b19ea7869808','VALIDO'),(218,19,15,19,1,1,10000.00,0.00,'2026-01-30 00:58:21','OK','',100,'20ab0afca0f84d7095fd87a7bd260063','VALIDO'),(219,19,15,19,1,1,30000.00,0.00,'2026-01-30 01:17:44','OK','',300,'61914cacf7e94198b27ddba55fcebaba','VALIDO'),(220,19,16,20,1,1,5000.00,0.00,'2026-01-30 15:48:09','OK','',50,'7a249bfb31724e80b8c8fba92613ab16','VALIDO'),(221,19,15,19,1,1,5000.00,0.00,'2026-02-01 15:55:08','OK','',0,'580f1fbdb1ac4a97b955296904ad3f26','VALIDO'),(222,19,15,19,1,1,10000.00,0.00,'2026-02-01 15:55:32','OK','',0,'3db9300ef2cf4d288a208bbfc40dd3d8','VALIDO'),(223,20,15,19,1,1,5000.00,0.00,'2026-02-01 16:02:54','OK','',0,'410a95ef3a8f4208a1d772580589857f','VALIDO'),(224,20,15,19,1,1,5000.00,0.00,'2026-02-01 16:03:48','OK','',0,'6a59bb27d30c4aa9a87c4714e8efe75a','VALIDO'),(225,20,15,19,1,1,5000.00,0.00,'2026-02-01 16:25:09','OK','',0,'38c99792fb634a16ac08a9c15483e560','VALIDO'),(226,20,15,19,1,1,10000.00,0.00,'2026-02-01 16:25:29','OK','',0,'c6394354eb824f7dad7acd98bb4dfb21','VALIDO'),(227,20,15,19,1,1,5000.00,0.00,'2026-02-01 16:28:44','OK','',0,'017430aee5544e5e8cda1435753ac56b','VALIDO'),(228,20,15,19,1,1,5000.00,0.00,'2026-02-01 16:30:10','OK','',0,'ee7a22cbace54b4b8afe97046739d345','VALIDO'),(229,20,15,19,1,1,5000.00,0.00,'2026-02-01 16:33:08','OK','',0,'30aa670a8df042d082e971713718d73a','VALIDO'),(230,20,15,19,1,1,5000.00,0.00,'2026-02-01 16:37:23','PENDIENTE','',0,'eed475f18dcc41e7ac8a365b9a9f7ded','VALIDO'),(231,20,15,19,1,1,5000.00,0.00,'2026-02-01 16:37:33','PENDIENTE','',0,'b9843d07a45e4462853269aa8b18adea','VALIDO'),(232,20,15,19,1,1,5000.00,0.00,'2026-02-01 17:03:15','PENDIENTE','',0,'c3c4402b0fee45ef91bffaac7da82b15','VALIDO'),(233,20,15,19,1,1,10000.00,0.00,'2026-02-01 17:03:25','PENDIENTE','',0,'e04f21aa011c4b8fa997a42cd36ef036','VALIDO'),(234,20,15,19,1,1,5000.00,0.00,'2026-02-01 17:36:23','OK','',50,'b9a7585c113d47d7bdeaab9c0bb43144','VALIDO'),(235,20,15,19,1,1,5000.00,0.00,'2026-02-01 18:13:01','OK','',50,'5b4f961c09064a5eaba1104dc8b0e6af','VALIDO'),(236,20,15,19,1,1,5000.00,0.00,'2026-02-01 18:18:32','OK','',50,'65a51851cc484ad0be784f95da033e0f','VALIDO'),(237,20,15,19,1,1,5000.00,0.00,'2026-02-01 18:24:57','OK','',50,'b9ddd644972d4d85b74236bf314f22b0','VALIDO'),(238,20,15,19,1,1,5000.00,0.00,'2026-02-01 18:34:23','OK','',50,'05986483f2c24b62b0b5ef370f19dea6','VALIDO'),(239,20,16,20,1,1,5000.00,0.00,'2026-02-01 18:36:37','OK','',50,'7a02bd3c938d4e58a7c909d79dd5d644','VALIDO'),(240,20,16,20,1,1,10000.00,0.00,'2026-02-01 18:44:43','OK','',100,'399afb95ea19437182535026ac7343fd','VALIDO'),(241,20,16,20,1,1,5000.00,0.00,'2026-02-01 18:45:12','OK','',50,'7d22d9951db740039e6253f496113845','VALIDO');
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas_detalle`
--

DROP TABLE IF EXISTS `ventas_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas_detalle` (
  `iddetalle` int NOT NULL AUTO_INCREMENT,
  `idventa` int NOT NULL,
  `idproductos` int NOT NULL,
  `cantidad` int NOT NULL DEFAULT '1',
  `precio_unitario` decimal(10,2) NOT NULL,
  `descuento` decimal(10,2) DEFAULT '0.00',
  `subtotal` decimal(10,2) NOT NULL,
  `cortesia` tinyint(1) DEFAULT '0',
  `autorizado` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `beneficio_aplicado` int DEFAULT NULL,
  PRIMARY KEY (`iddetalle`),
  KEY `idventa` (`idventa`),
  KEY `idproductos` (`idproductos`),
  KEY `beneficio_aplicado` (`beneficio_aplicado`),
  CONSTRAINT `ventas_detalle_ibfk_1` FOREIGN KEY (`idventa`) REFERENCES `ventas` (`idventa`),
  CONSTRAINT `ventas_detalle_ibfk_2` FOREIGN KEY (`idproductos`) REFERENCES `productos` (`idproductos`),
  CONSTRAINT `ventas_detalle_ibfk_3` FOREIGN KEY (`beneficio_aplicado`) REFERENCES `puntos_beneficios` (`idbeneficio`)
) ENGINE=InnoDB AUTO_INCREMENT=308 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas_detalle`
--

LOCK TABLES `ventas_detalle` WRITE;
/*!40000 ALTER TABLE `ventas_detalle` DISABLE KEYS */;
INSERT INTO `ventas_detalle` VALUES (1,3,5,1,7000.00,0.00,7000.00,0,NULL,NULL),(2,3,8,1,7000.00,0.00,7000.00,0,NULL,NULL),(3,4,2,1,5000.00,0.00,5000.00,0,NULL,NULL),(4,4,16,1,20000.00,0.00,20000.00,0,NULL,NULL),(5,5,5,1,7000.00,0.00,7000.00,0,NULL,NULL),(6,5,7,1,7000.00,0.00,7000.00,0,NULL,NULL),(7,5,8,1,7000.00,0.00,0.00,1,NULL,NULL),(8,6,7,1,7000.00,0.00,0.00,1,NULL,NULL),(9,6,8,1,7000.00,0.00,7000.00,0,NULL,NULL),(10,7,7,1,7000.00,0.00,7000.00,0,NULL,NULL),(11,7,16,1,20000.00,0.00,20000.00,0,NULL,NULL),(12,7,5,1,7000.00,0.00,7000.00,0,NULL,NULL),(13,8,16,1,20000.00,0.00,20000.00,0,NULL,NULL),(14,8,6,1,8000.00,0.00,8000.00,0,NULL,NULL),(15,9,3,1,37000.00,0.00,37000.00,0,NULL,NULL),(16,9,6,1,8000.00,0.00,8000.00,0,NULL,NULL),(17,10,9,2,5000.00,0.00,10000.00,0,NULL,NULL),(18,11,6,1,8000.00,0.00,8000.00,0,NULL,NULL),(19,11,4,1,8000.00,0.00,8000.00,0,NULL,NULL),(20,12,10,1,7000.00,0.00,7000.00,0,NULL,NULL),(21,13,6,1,8000.00,0.00,8000.00,0,NULL,NULL),(22,14,4,1,8000.00,0.00,8000.00,0,NULL,NULL),(23,15,6,1,8000.00,0.00,8000.00,0,NULL,NULL),(24,16,6,1,8000.00,0.00,8000.00,0,NULL,NULL),(25,16,14,1,6000.00,0.00,6000.00,0,NULL,NULL),(26,17,10,1,7000.00,0.00,7000.00,0,NULL,NULL),(27,17,14,1,6000.00,0.00,6000.00,0,NULL,NULL),(28,18,10,1,7000.00,0.00,7000.00,0,NULL,NULL),(29,18,14,1,6000.00,0.00,6000.00,0,NULL,NULL),(30,19,14,1,6000.00,0.00,6000.00,0,NULL,NULL),(31,19,8,1,7000.00,0.00,7000.00,0,NULL,NULL),(32,20,8,1,7000.00,0.00,7000.00,0,NULL,NULL),(33,20,14,1,6000.00,0.00,6000.00,0,NULL,NULL),(34,20,2,1,5000.00,0.00,5000.00,0,NULL,NULL),(35,21,9,1,5000.00,0.00,5000.00,0,NULL,NULL),(36,21,14,1,6000.00,0.00,6000.00,0,NULL,NULL),(37,22,6,1,8000.00,0.00,8000.00,0,NULL,NULL),(38,22,14,1,6000.00,0.00,6000.00,0,NULL,NULL),(39,23,4,1,8000.00,0.00,8000.00,0,NULL,NULL),(40,23,6,1,8000.00,0.00,8000.00,0,NULL,NULL),(41,24,3,1,37000.00,0.00,37000.00,0,NULL,NULL),(42,25,17,1,8000.00,0.00,8000.00,0,NULL,NULL),(43,25,9,1,5000.00,0.00,5000.00,0,NULL,NULL),(44,26,9,1,5000.00,0.00,5000.00,0,NULL,NULL),(45,26,8,1,7000.00,0.00,7000.00,0,NULL,NULL),(46,27,2,1,5000.00,0.00,5000.00,0,NULL,NULL),(47,27,14,1,6000.00,0.00,6000.00,0,NULL,NULL),(48,28,9,1,5000.00,0.00,5000.00,0,NULL,NULL),(49,28,8,1,7000.00,0.00,7000.00,0,NULL,NULL),(50,29,2,1,5000.00,0.00,5000.00,0,NULL,NULL),(51,29,1,1,10000.00,0.00,10000.00,0,NULL,NULL),(52,30,8,1,7000.00,0.00,7000.00,0,NULL,NULL),(53,31,8,1,7000.00,0.00,7000.00,0,NULL,NULL),(54,31,17,1,8000.00,0.00,8000.00,0,NULL,NULL),(55,32,6,1,8000.00,0.00,8000.00,0,NULL,NULL),(56,33,7,1,7000.00,0.00,7000.00,0,NULL,NULL),(57,34,4,1,8000.00,0.00,8000.00,0,NULL,NULL),(58,34,6,1,8000.00,0.00,8000.00,0,NULL,NULL),(59,35,17,1,8000.00,0.00,8000.00,0,NULL,NULL),(60,35,9,1,5000.00,0.00,5000.00,0,NULL,NULL),(61,36,14,1,6000.00,0.00,6000.00,0,NULL,NULL),(62,36,17,1,8000.00,0.00,8000.00,0,NULL,NULL),(63,37,3,1,37000.00,0.00,37000.00,0,NULL,NULL),(64,38,15,1,8000.00,0.00,8000.00,0,NULL,NULL),(65,38,7,1,7000.00,0.00,7000.00,0,NULL,NULL),(66,38,17,1,8000.00,0.00,8000.00,0,NULL,NULL),(67,39,17,1,8000.00,0.00,8000.00,0,NULL,NULL),(68,40,17,1,8000.00,0.00,8000.00,0,NULL,NULL),(69,41,17,1,8000.00,0.00,8000.00,0,NULL,NULL),(70,42,17,1,8000.00,0.00,8000.00,0,NULL,NULL),(71,42,9,1,5000.00,0.00,5000.00,0,NULL,NULL),(72,42,15,1,8000.00,0.00,8000.00,0,NULL,NULL),(73,42,14,1,6000.00,0.00,6000.00,0,NULL,NULL),(74,43,3,1,37000.00,0.00,37000.00,0,NULL,NULL),(75,43,10,1,7000.00,0.00,7000.00,0,NULL,NULL),(76,44,7,1,7000.00,0.00,7000.00,0,NULL,NULL),(77,44,18,1,12000.00,0.00,12000.00,0,NULL,NULL),(78,45,9,1,5000.00,0.00,5000.00,0,NULL,NULL),(79,46,7,1,7000.00,0.00,7000.00,0,NULL,NULL),(80,46,14,1,6000.00,0.00,0.00,1,NULL,NULL),(81,47,7,1,7000.00,0.00,7000.00,0,NULL,NULL),(82,47,18,1,12000.00,0.00,12000.00,0,NULL,NULL),(83,48,15,1,8000.00,0.00,8000.00,0,NULL,NULL),(84,49,5,1,7000.00,0.00,0.00,1,NULL,NULL),(85,49,11,1,9000.00,0.00,9000.00,0,NULL,NULL),(86,50,3,1,37000.00,0.00,37000.00,0,NULL,NULL),(87,51,9,1,5000.00,0.00,5000.00,0,NULL,NULL),(88,51,11,1,9000.00,0.00,9000.00,0,NULL,NULL),(89,52,8,1,7000.00,0.00,7000.00,0,NULL,NULL),(90,52,12,1,18000.00,0.00,18000.00,0,NULL,NULL),(91,53,8,1,7000.00,0.00,7000.00,0,NULL,NULL),(92,54,7,1,7000.00,0.00,7000.00,0,NULL,NULL),(93,55,10,1,7000.00,0.00,7000.00,0,NULL,NULL),(94,56,10,1,7000.00,0.00,7000.00,0,NULL,NULL),(95,57,15,1,8000.00,0.00,8000.00,0,NULL,NULL),(96,58,12,1,18000.00,0.00,18000.00,0,NULL,NULL),(97,59,9,1,5000.00,0.00,5000.00,0,NULL,NULL),(98,60,3,1,37000.00,0.00,37000.00,0,NULL,NULL),(99,61,1,1,10000.00,0.00,10000.00,0,NULL,NULL),(100,62,1,1,10000.00,0.00,0.00,1,NULL,NULL),(101,63,17,2,8000.00,0.00,16000.00,0,NULL,NULL),(102,64,12,1,18000.00,0.00,18000.00,0,NULL,NULL),(103,64,7,2,7000.00,0.00,14000.00,0,NULL,NULL),(104,64,15,1,8000.00,0.00,8000.00,0,NULL,NULL),(105,65,3,1,37000.00,0.00,37000.00,0,NULL,NULL),(106,66,6,1,8000.00,0.00,8000.00,0,NULL,NULL),(107,67,5,1,7000.00,0.00,7000.00,0,NULL,NULL),(108,68,7,1,7000.00,0.00,7000.00,0,NULL,NULL),(109,69,8,1,7000.00,0.00,7000.00,0,NULL,NULL),(110,70,5,1,7000.00,0.00,7000.00,0,NULL,NULL),(111,71,7,1,7000.00,0.00,7000.00,0,NULL,NULL),(112,72,8,1,7000.00,0.00,7000.00,0,NULL,NULL),(113,73,8,1,7000.00,0.00,7000.00,0,NULL,NULL),(114,74,12,1,18000.00,0.00,18000.00,0,NULL,NULL),(115,75,13,1,9000.00,0.00,9000.00,0,NULL,NULL),(116,76,1,1,10000.00,0.00,10000.00,0,NULL,NULL),(117,77,3,1,37000.00,0.00,37000.00,0,NULL,NULL),(118,78,12,1,18000.00,0.00,18000.00,0,NULL,NULL),(119,79,12,1,18000.00,0.00,18000.00,0,NULL,NULL),(120,80,13,1,9000.00,0.00,9000.00,0,NULL,NULL),(121,81,13,1,9000.00,0.00,9000.00,0,NULL,NULL),(122,82,14,1,6000.00,0.00,6000.00,0,NULL,NULL),(123,82,6,1,8000.00,0.00,8000.00,0,NULL,NULL),(124,83,6,1,8000.00,0.00,8000.00,0,NULL,NULL),(125,83,12,1,18000.00,0.00,18000.00,0,NULL,NULL),(126,84,14,1,6000.00,0.00,6000.00,0,NULL,NULL),(127,84,11,1,9000.00,0.00,9000.00,0,NULL,NULL),(128,85,5,1,7000.00,0.00,7000.00,0,NULL,NULL),(129,85,10,1,7000.00,0.00,7000.00,0,NULL,NULL),(130,86,13,1,9000.00,0.00,9000.00,0,NULL,NULL),(131,86,18,1,12000.00,0.00,12000.00,0,NULL,NULL),(132,87,6,1,8000.00,0.00,8000.00,0,NULL,NULL),(133,87,11,1,9000.00,0.00,9000.00,0,NULL,NULL),(134,88,10,1,7000.00,0.00,7000.00,0,NULL,NULL),(135,88,9,1,5000.00,0.00,5000.00,0,NULL,NULL),(136,89,13,1,9000.00,0.00,9000.00,0,NULL,NULL),(137,89,14,1,6000.00,0.00,6000.00,0,NULL,NULL),(138,90,16,1,20000.00,0.00,20000.00,0,NULL,NULL),(139,90,10,1,7000.00,0.00,7000.00,0,NULL,NULL),(140,91,15,1,8000.00,0.00,8000.00,0,NULL,NULL),(141,92,13,1,9000.00,0.00,9000.00,0,NULL,NULL),(142,93,14,1,6000.00,0.00,6000.00,0,NULL,NULL),(143,94,7,1,7000.00,0.00,7000.00,0,NULL,NULL),(144,94,14,1,6000.00,0.00,6000.00,0,NULL,NULL),(145,95,6,1,8000.00,0.00,8000.00,0,NULL,NULL),(146,95,14,1,6000.00,0.00,6000.00,0,NULL,NULL),(147,96,4,1,8000.00,0.00,8000.00,0,NULL,NULL),(148,97,10,1,7000.00,0.00,7000.00,0,NULL,NULL),(149,98,10,1,7000.00,0.00,7000.00,0,NULL,NULL),(150,99,9,1,5000.00,0.00,5000.00,0,NULL,NULL),(151,100,7,1,7000.00,0.00,0.00,1,'gustavo peñalba',NULL),(152,101,15,1,8000.00,0.00,0.00,1,'gustavo peñalba',NULL),(153,102,15,1,8000.00,0.00,0.00,1,'gustavo peñalba',NULL),(154,103,7,1,7000.00,0.00,0.00,1,'gustavo peñalba',NULL),(155,104,7,1,7000.00,0.00,7000.00,0,NULL,NULL),(156,105,6,1,8000.00,0.00,8000.00,0,NULL,NULL),(157,106,6,1,8000.00,0.00,8000.00,0,NULL,NULL),(158,107,5,1,7000.00,0.00,7000.00,0,NULL,NULL),(159,108,6,1,8000.00,0.00,8000.00,0,NULL,NULL),(160,109,7,1,7000.00,0.00,7000.00,0,NULL,NULL),(161,110,7,1,7000.00,0.00,7000.00,0,NULL,NULL),(162,111,7,1,7000.00,0.00,7000.00,0,NULL,NULL),(163,112,16,1,20000.00,0.00,20000.00,0,NULL,NULL),(164,113,7,1,7000.00,0.00,0.00,1,NULL,NULL),(165,114,7,1,7000.00,0.00,7000.00,0,'',NULL),(166,115,7,1,7000.00,0.00,0.00,1,'gustavo peñalba',NULL),(167,116,15,1,8000.00,0.00,8000.00,0,'',NULL),(168,116,6,1,8000.00,0.00,0.00,1,'gustavo peñalba',NULL),(169,117,9,1,5000.00,0.00,5000.00,0,'',NULL),(170,118,6,1,8000.00,0.00,0.00,1,'GUSTAVO PEÑALBA',NULL),(171,118,13,1,9000.00,0.00,9000.00,0,'',NULL),(172,120,7,1,7000.00,0.00,7000.00,0,'',NULL),(173,121,16,1,20000.00,0.00,20000.00,0,'',NULL),(174,122,7,1,7000.00,0.00,7000.00,0,'',NULL),(175,123,15,1,8000.00,0.00,8000.00,0,'',NULL),(176,124,16,1,20000.00,0.00,20000.00,0,'',NULL),(177,124,14,1,6000.00,0.00,6000.00,0,'',NULL),(178,125,9,1,5000.00,0.00,5000.00,0,'',NULL),(179,126,16,1,20000.00,0.00,20000.00,0,'',NULL),(180,127,14,1,6000.00,0.00,6000.00,0,'',NULL),(181,128,15,1,8000.00,0.00,8000.00,0,'',NULL),(182,129,16,1,20000.00,0.00,20000.00,0,'',NULL),(183,130,15,1,8000.00,0.00,8000.00,0,'',NULL),(184,131,14,1,6000.00,0.00,6000.00,0,'',NULL),(185,132,12,1,18000.00,0.00,18000.00,0,'',NULL),(186,133,16,1,20000.00,0.00,20000.00,0,'',NULL),(187,134,15,1,8000.00,0.00,8000.00,0,'',NULL),(188,135,15,1,8000.00,0.00,8000.00,0,'',NULL),(189,135,14,1,6000.00,0.00,6000.00,0,'',NULL),(190,136,14,2,6000.00,0.00,12000.00,0,'',NULL),(191,137,14,1,6000.00,0.00,6000.00,0,'',NULL),(192,137,6,1,8000.00,0.00,8000.00,0,'',NULL),(193,138,6,1,8000.00,0.00,8000.00,0,'',NULL),(194,138,7,1,7000.00,0.00,7000.00,0,'',NULL),(195,139,15,1,8000.00,0.00,8000.00,0,'',NULL),(196,139,13,1,9000.00,0.00,9000.00,0,'',NULL),(197,140,16,1,20000.00,0.00,20000.00,0,'',NULL),(198,141,15,1,8000.00,0.00,8000.00,0,'',NULL),(199,142,2,1,5000.00,0.00,5000.00,0,'',NULL),(200,143,15,1,8000.00,0.00,8000.00,0,'',NULL),(201,143,14,1,6000.00,0.00,6000.00,0,'',NULL),(202,144,15,1,8000.00,0.00,8000.00,0,'',NULL),(203,145,16,1,20000.00,0.00,20000.00,0,'',NULL),(204,146,16,1,20000.00,0.00,20000.00,0,'',NULL),(205,147,15,1,8000.00,0.00,8000.00,0,'',NULL),(206,147,13,1,9000.00,0.00,9000.00,0,'',NULL),(207,148,15,1,8000.00,0.00,8000.00,0,'',NULL),(208,149,7,1,7000.00,0.00,7000.00,0,'',NULL),(209,150,4,1,8000.00,0.00,8000.00,0,'',NULL),(210,150,12,1,18000.00,0.00,18000.00,0,'',NULL),(211,151,15,1,8000.00,0.00,8000.00,0,'',NULL),(212,152,7,1,7000.00,0.00,7000.00,0,'',NULL),(213,152,9,1,5000.00,0.00,5000.00,0,'',NULL),(214,153,15,1,8000.00,0.00,8000.00,0,'',NULL),(215,154,15,1,8000.00,0.00,8000.00,0,'',NULL),(216,154,13,1,9000.00,0.00,9000.00,0,'',NULL),(217,155,16,1,20000.00,0.00,20000.00,0,'',NULL),(218,155,14,1,6000.00,0.00,6000.00,0,'',NULL),(219,156,16,1,20000.00,0.00,20000.00,0,'',NULL),(220,156,15,1,8000.00,0.00,8000.00,0,'',NULL),(221,157,7,1,7000.00,0.00,7000.00,0,'',NULL),(222,157,6,1,8000.00,0.00,8000.00,0,'',NULL),(223,158,13,1,9000.00,0.00,9000.00,0,'',NULL),(224,159,13,1,9000.00,0.00,9000.00,0,'',NULL),(225,160,16,1,20000.00,0.00,20000.00,0,'',NULL),(226,161,15,1,8000.00,0.00,8000.00,0,'',NULL),(227,162,15,1,8000.00,0.00,8000.00,0,'',NULL),(228,163,5,1,7000.00,0.00,7000.00,0,'',NULL),(229,163,6,1,8000.00,0.00,8000.00,0,'',NULL),(230,164,6,1,8000.00,0.00,8000.00,0,'',NULL),(231,165,5,1,7000.00,0.00,7000.00,0,'',NULL),(232,165,6,1,8000.00,0.00,8000.00,0,'',NULL),(233,166,7,1,7000.00,0.00,7000.00,0,'',NULL),(234,167,6,1,8000.00,0.00,8000.00,0,'',NULL),(235,168,6,1,8000.00,0.00,8000.00,0,'',NULL),(236,169,16,1,20000.00,0.00,0.00,1,'',NULL),(237,169,7,1,7000.00,0.00,7000.00,0,'',NULL),(238,170,16,1,20000.00,0.00,20000.00,0,'',NULL),(239,171,6,1,8000.00,0.00,8000.00,0,'',NULL),(240,172,5,1,7000.00,0.00,7000.00,0,'',NULL),(241,173,7,1,7000.00,0.00,0.00,1,'gustavo',NULL),(242,174,7,1,7000.00,0.00,7000.00,0,'',NULL),(243,175,9,1,5000.00,0.00,5000.00,0,'',NULL),(244,176,16,1,20000.00,0.00,20000.00,0,'',NULL),(245,177,6,1,8000.00,0.00,8000.00,0,'',NULL),(246,178,9,1,5000.00,0.00,5000.00,0,'',NULL),(247,179,15,1,8000.00,0.00,0.00,1,'gustavo peñalba',NULL),(248,180,7,1,7000.00,0.00,0.00,1,'gustavo',NULL),(249,181,7,1,7000.00,0.00,7000.00,0,'',NULL),(250,182,15,1,8000.00,0.00,8000.00,0,'',NULL),(251,183,14,1,6000.00,0.00,6000.00,0,'',NULL),(252,183,13,1,9000.00,0.00,9000.00,0,'',NULL),(253,183,12,1,18000.00,0.00,18000.00,0,'',NULL),(254,184,12,1,18000.00,0.00,18000.00,0,'',NULL),(255,185,14,1,6000.00,0.00,6000.00,0,'',NULL),(256,186,12,1,18000.00,0.00,18000.00,0,'',NULL),(257,187,6,1,8000.00,0.00,8000.00,0,'',NULL),(258,188,10,1,7000.00,0.00,7000.00,0,'',NULL),(259,189,11,1,9000.00,0.00,9000.00,0,'',NULL),(260,189,3,1,37000.00,0.00,37000.00,0,'',NULL),(261,190,13,1,9000.00,0.00,9000.00,0,'',NULL),(262,190,1,1,10000.00,0.00,10000.00,0,'',NULL),(263,191,12,1,18000.00,0.00,18000.00,0,'',NULL),(264,192,13,1,9000.00,0.00,0.00,1,'gustavo peñalba',NULL),(265,193,5,1,7000.00,0.00,7000.00,0,'',NULL),(266,194,11,1,9000.00,0.00,9000.00,0,'',NULL),(267,196,2,1,5000.00,0.00,5000.00,0,'',NULL),(268,197,5,1,7000.00,0.00,7000.00,0,'',NULL),(269,204,2,1,5000.00,0.00,5000.00,0,'',NULL),(270,205,5,1,7000.00,0.00,7000.00,0,'',NULL),(271,206,5,1,7000.00,0.00,7000.00,0,'',NULL),(272,207,5,1,7000.00,0.00,7000.00,0,'',NULL),(273,208,5,1,7000.00,0.00,7000.00,0,'',NULL),(274,209,2,1,5000.00,0.00,5000.00,0,'',NULL),(275,210,5,1,7000.00,0.00,7000.00,0,'',NULL),(276,211,2,1,5000.00,0.00,5000.00,0,'',NULL),(277,212,1,1,10000.00,0.00,10000.00,0,'',NULL),(278,213,1,1,10000.00,0.00,10000.00,0,'',NULL),(279,214,2,1,5000.00,0.00,5000.00,0,'',NULL),(280,215,5,1,7000.00,0.00,7000.00,0,'',NULL),(281,216,5,1,7000.00,0.00,7000.00,0,'',NULL),(282,217,2,1,5000.00,0.00,5000.00,0,'',NULL),(283,218,1,1,10000.00,0.00,10000.00,0,'',NULL),(284,219,2,2,5000.00,0.00,10000.00,0,'',NULL),(285,219,1,2,10000.00,0.00,20000.00,0,'',NULL),(286,220,2,1,5000.00,0.00,5000.00,0,'',NULL),(287,221,2,1,5000.00,0.00,5000.00,0,'',NULL),(288,222,1,1,10000.00,0.00,10000.00,0,'',NULL),(289,223,2,1,5000.00,0.00,5000.00,0,'',NULL),(290,224,2,1,5000.00,0.00,5000.00,0,'',NULL),(291,225,2,1,5000.00,0.00,5000.00,0,'',NULL),(292,226,2,2,5000.00,0.00,10000.00,0,'',NULL),(293,227,2,1,5000.00,0.00,5000.00,0,'',NULL),(294,228,2,1,5000.00,0.00,5000.00,0,'',NULL),(295,229,2,1,5000.00,0.00,5000.00,0,'',NULL),(296,230,2,1,5000.00,0.00,5000.00,0,'',NULL),(297,231,2,1,5000.00,0.00,5000.00,0,'',NULL),(298,232,2,1,5000.00,0.00,5000.00,0,'',NULL),(299,233,1,1,10000.00,0.00,10000.00,0,'',NULL),(300,234,2,1,5000.00,0.00,5000.00,0,'',NULL),(301,235,2,1,5000.00,0.00,5000.00,0,'',NULL),(302,236,2,1,5000.00,0.00,5000.00,0,'',NULL),(303,237,2,1,5000.00,0.00,5000.00,0,'',NULL),(304,238,2,1,5000.00,0.00,5000.00,0,'',NULL),(305,239,2,1,5000.00,0.00,5000.00,0,'',NULL),(306,240,1,1,10000.00,0.00,10000.00,0,'',NULL),(307,241,2,1,5000.00,0.00,5000.00,0,'',NULL);
/*!40000 ALTER TABLE `ventas_detalle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas_entradas`
--

DROP TABLE IF EXISTS `ventas_entradas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas_entradas` (
  `idventa` int NOT NULL AUTO_INCREMENT,
  `idjornada` int NOT NULL,
  `idusuario` int NOT NULL,
  `cliente` int NOT NULL DEFAULT '1',
  `idmodopago` int DEFAULT NULL,
  `fecha_emision` datetime DEFAULT CURRENT_TIMESTAMP,
  `total` decimal(10,2) NOT NULL,
  `estado` enum('OK','ANULADA') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'OK',
  PRIMARY KEY (`idventa`),
  KEY `idjornada` (`idjornada`),
  KEY `idusuario` (`idusuario`),
  KEY `fk_ventas_entradas_cliente` (`cliente`),
  CONSTRAINT `fk_ventas_entradas_cliente` FOREIGN KEY (`cliente`) REFERENCES `clientes` (`idclientes`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `ventas_entradas_ibfk_1` FOREIGN KEY (`idjornada`) REFERENCES `jornadas` (`idjornada`)
) ENGINE=InnoDB AUTO_INCREMENT=157 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas_entradas`
--

LOCK TABLES `ventas_entradas` WRITE;
/*!40000 ALTER TABLE `ventas_entradas` DISABLE KEYS */;
INSERT INTO `ventas_entradas` VALUES (4,13,7,1,NULL,'2026-01-15 19:34:12',6000.00,'OK'),(5,13,7,1,NULL,'2026-01-15 19:45:30',3000.00,'OK'),(6,13,7,1,NULL,'2026-01-15 21:35:33',3000.00,'OK'),(7,13,7,1,NULL,'2026-01-15 21:39:51',3000.00,'OK'),(8,13,7,1,NULL,'2026-01-15 21:42:58',4500.00,'OK'),(9,13,7,1,NULL,'2026-01-15 21:48:43',4500.00,'OK'),(10,13,7,1,NULL,'2026-01-15 21:50:26',4500.00,'OK'),(11,13,7,1,NULL,'2026-01-15 21:51:22',3000.00,'OK'),(12,13,7,1,NULL,'2026-01-15 21:56:50',3000.00,'OK'),(13,13,7,1,NULL,'2026-01-15 23:12:01',6000.00,'OK'),(14,13,7,1,NULL,'2026-01-15 23:15:38',3000.00,'OK'),(15,13,7,1,NULL,'2026-01-15 23:17:30',3000.00,'OK'),(16,13,7,1,NULL,'2026-01-15 23:30:02',3000.00,'OK'),(17,13,7,1,NULL,'2026-01-15 23:31:13',3000.00,'OK'),(18,13,7,1,NULL,'2026-01-15 23:51:21',4500.00,'OK'),(19,13,7,1,NULL,'2026-01-15 23:56:17',4500.00,'OK'),(20,13,7,1,NULL,'2026-01-16 00:13:28',3000.00,'OK'),(21,13,7,1,NULL,'2026-01-16 00:29:21',4500.00,'OK'),(22,13,7,1,NULL,'2026-01-16 00:41:45',6000.00,'OK'),(23,13,7,1,NULL,'2026-01-16 00:43:30',3000.00,'OK'),(24,13,7,5,NULL,'2026-01-16 01:34:59',3000.00,'OK'),(25,13,7,6,NULL,'2026-01-16 01:36:30',3000.00,'OK'),(26,13,7,6,NULL,'2026-01-16 07:42:53',3000.00,'OK'),(27,13,7,5,NULL,'2026-01-16 07:44:11',3000.00,'OK'),(28,15,15,1,NULL,'2026-01-24 09:31:10',3000.00,'OK'),(29,15,15,1,NULL,'2026-01-24 09:35:03',3000.00,'OK'),(30,17,15,1,1,'2026-01-28 15:15:46',3000.00,'OK'),(31,17,15,6,1,'2026-01-28 15:16:50',3000.00,'OK'),(32,17,15,1,1,'2026-01-28 15:21:12',3000.00,'OK'),(33,17,15,1,NULL,'2026-01-28 15:22:38',3000.00,'OK'),(34,17,15,1,NULL,'2026-01-28 15:22:38',3000.00,'OK'),(35,17,15,1,1,'2026-01-28 15:27:07',3000.00,'OK'),(36,17,15,1,1,'2026-01-28 15:31:08',3000.00,'OK'),(37,17,15,1,1,'2026-01-28 15:32:07',3000.00,'OK'),(38,17,15,1,1,'2026-01-28 15:33:16',3000.00,'OK'),(39,17,15,1,1,'2026-01-28 15:35:25',3000.00,'OK'),(40,17,15,1,1,'2026-01-28 15:35:38',3000.00,'OK'),(41,17,15,1,1,'2026-01-28 15:39:53',3000.00,'OK'),(42,17,15,1,1,'2026-01-28 15:40:14',3000.00,'OK'),(43,17,15,1,NULL,'2026-01-28 15:40:43',3000.00,'OK'),(44,17,15,1,NULL,'2026-01-28 15:40:43',3000.00,'OK'),(45,17,15,1,1,'2026-01-28 15:45:08',3000.00,'OK'),(46,18,15,1,1,'2026-01-28 15:47:41',3000.00,'OK'),(47,18,15,1,1,'2026-01-28 15:49:30',3000.00,'OK'),(48,18,15,1,1,'2026-01-28 15:51:28',3000.00,'OK'),(49,18,15,1,1,'2026-01-28 15:55:31',3000.00,'OK'),(50,18,15,1,1,'2026-01-28 16:06:32',3000.00,'OK'),(51,18,15,1,NULL,'2026-01-28 16:07:04',3000.00,'OK'),(52,18,15,1,NULL,'2026-01-28 16:07:04',3000.00,'OK'),(53,18,15,1,1,'2026-01-28 16:11:38',3000.00,'OK'),(54,18,15,1,1,'2026-01-28 16:17:20',3000.00,'OK'),(55,18,15,1,1,'2026-01-28 16:18:16',3000.00,'OK'),(56,18,15,1,1,'2026-01-28 16:18:39',3000.00,'OK'),(57,18,15,1,1,'2026-01-28 16:18:56',3000.00,'OK'),(58,18,15,1,1,'2026-01-28 16:19:12',3000.00,'OK'),(59,18,15,1,1,'2026-01-28 16:33:56',3000.00,'OK'),(60,18,15,1,1,'2026-01-28 16:37:25',3000.00,'OK'),(61,18,15,1,1,'2026-01-28 16:42:13',3000.00,'OK'),(62,18,15,1,NULL,'2026-01-28 16:42:37',3000.00,'OK'),(63,18,15,1,NULL,'2026-01-28 16:42:37',3000.00,'OK'),(64,18,15,1,1,'2026-01-28 16:43:24',3000.00,'OK'),(65,18,15,1,NULL,'2026-01-28 16:43:45',3000.00,'OK'),(66,18,15,1,NULL,'2026-01-28 16:43:45',3000.00,'OK'),(67,18,15,1,1,'2026-01-28 16:50:44',3000.00,'OK'),(68,18,15,1,NULL,'2026-01-28 16:51:08',3000.00,'OK'),(69,18,15,1,NULL,'2026-01-28 16:51:08',3000.00,'OK'),(70,18,15,1,1,'2026-01-28 16:51:27',3000.00,'OK'),(71,18,15,1,NULL,'2026-01-28 16:56:34',3000.00,'OK'),(72,18,15,1,NULL,'2026-01-28 17:11:05',3000.00,'OK'),(73,18,15,1,NULL,'2026-01-28 17:11:35',3000.00,'OK'),(74,18,15,1,NULL,'2026-01-28 17:11:35',3000.00,'OK'),(75,18,15,1,NULL,'2026-01-28 17:23:00',3000.00,'OK'),(76,18,15,1,NULL,'2026-01-28 17:23:00',3000.00,'OK'),(77,18,15,1,NULL,'2026-01-28 17:23:49',3000.00,'OK'),(78,18,15,1,NULL,'2026-01-28 17:23:49',3000.00,'OK'),(79,18,15,1,NULL,'2026-01-28 17:25:26',3000.00,'OK'),(80,18,15,1,NULL,'2026-01-28 17:25:26',3000.00,'OK'),(81,18,15,1,1,'2026-01-28 17:29:27',3000.00,'OK'),(82,18,15,1,1,'2026-01-28 17:33:18',3000.00,'OK'),(83,18,15,1,1,'2026-01-28 17:33:18',3000.00,'OK'),(84,18,15,1,NULL,'2026-01-28 17:33:59',3000.00,'OK'),(85,18,15,1,NULL,'2026-01-28 17:33:59',3000.00,'OK'),(86,18,15,1,1,'2026-01-28 17:34:39',3000.00,'OK'),(87,18,15,1,1,'2026-01-28 17:34:39',3000.00,'OK'),(88,18,15,1,NULL,'2026-01-28 17:44:39',3000.00,'OK'),(89,18,15,1,NULL,'2026-01-28 17:44:39',3000.00,'OK'),(90,18,15,1,1,'2026-01-28 17:45:01',3000.00,'OK'),(91,18,15,1,1,'2026-01-28 17:45:01',3000.00,'OK'),(92,18,15,1,1,'2026-01-28 17:45:20',3000.00,'OK'),(93,18,15,1,1,'2026-01-28 17:45:20',3000.00,'OK'),(94,18,15,1,NULL,'2026-01-28 17:45:47',3000.00,'OK'),(95,18,15,1,NULL,'2026-01-28 17:45:47',3000.00,'OK'),(96,18,15,1,1,'2026-01-28 17:56:37',3000.00,'OK'),(97,18,15,1,1,'2026-01-28 17:56:37',3000.00,'OK'),(98,18,15,1,1,'2026-01-28 17:59:29',3000.00,'OK'),(99,18,15,1,1,'2026-01-28 17:59:29',3000.00,'OK'),(100,18,15,1,1,'2026-01-28 18:01:58',3000.00,'OK'),(101,18,15,1,1,'2026-01-28 18:01:58',3000.00,'OK'),(102,18,15,1,NULL,'2026-01-28 18:07:39',3000.00,'OK'),(103,18,15,1,NULL,'2026-01-28 18:07:39',3000.00,'OK'),(104,18,15,1,1,'2026-01-28 18:08:18',3000.00,'OK'),(105,18,15,1,1,'2026-01-28 18:08:18',3000.00,'OK'),(106,18,15,5,NULL,'2026-01-28 18:14:42',3000.00,'OK'),(107,18,15,5,NULL,'2026-01-28 18:14:42',3000.00,'OK'),(108,18,15,1,1,'2026-01-28 18:18:32',3000.00,'OK'),(109,18,15,1,1,'2026-01-28 18:18:32',3000.00,'OK'),(110,18,15,1,1,'2026-01-28 18:21:44',3000.00,'OK'),(111,18,15,1,1,'2026-01-28 18:21:44',3000.00,'OK'),(112,18,15,1,1,'2026-01-28 18:23:07',3000.00,'OK'),(113,18,15,1,1,'2026-01-28 18:23:07',3000.00,'OK'),(114,18,15,1,1,'2026-01-28 18:23:41',3000.00,'OK'),(115,18,15,1,1,'2026-01-28 18:23:41',3000.00,'OK'),(116,18,15,1,1,'2026-01-28 18:25:41',3000.00,'OK'),(117,18,15,1,1,'2026-01-28 18:25:41',3000.00,'OK'),(118,18,15,1,1,'2026-01-28 18:26:31',3000.00,'OK'),(119,18,15,1,1,'2026-01-28 18:26:31',3000.00,'OK'),(120,18,15,1,1,'2026-01-28 18:33:33',3000.00,'OK'),(121,18,15,1,1,'2026-01-28 18:33:33',3000.00,'OK'),(122,18,15,1,1,'2026-01-28 18:35:15',3000.00,'OK'),(123,18,15,1,1,'2026-01-28 18:35:15',3000.00,'OK'),(124,18,15,1,1,'2026-01-28 18:35:48',3000.00,'OK'),(125,18,15,1,1,'2026-01-28 18:35:48',3000.00,'OK'),(126,18,15,1,1,'2026-01-28 18:36:49',3000.00,'OK'),(127,18,15,1,1,'2026-01-28 18:36:49',3000.00,'OK'),(128,18,15,1,1,'2026-01-28 18:37:06',3000.00,'OK'),(129,18,15,1,1,'2026-01-28 18:37:06',3000.00,'OK'),(130,18,15,1,NULL,'2026-01-28 18:37:49',3000.00,'OK'),(131,18,15,1,NULL,'2026-01-28 18:37:49',3000.00,'OK'),(132,18,15,1,1,'2026-01-28 18:38:08',3000.00,'OK'),(133,18,15,1,1,'2026-01-28 18:38:08',3000.00,'OK'),(134,18,15,1,1,'2026-01-28 18:38:45',3000.00,'OK'),(135,18,15,1,1,'2026-01-28 18:38:45',3000.00,'OK'),(136,18,15,1,1,'2026-01-28 18:44:05',3000.00,'OK'),(137,18,15,1,1,'2026-01-28 18:44:05',3000.00,'OK'),(138,18,15,1,1,'2026-01-28 18:44:25',3000.00,'OK'),(139,18,15,1,1,'2026-01-28 18:44:25',3000.00,'OK'),(140,18,15,1,1,'2026-01-28 18:48:35',3000.00,'OK'),(141,18,15,1,1,'2026-01-28 18:48:52',3000.00,'OK'),(142,18,15,1,1,'2026-01-28 18:49:03',3000.00,'OK'),(143,18,15,1,1,'2026-01-28 22:32:41',3000.00,'OK'),(144,18,15,5,NULL,'2026-01-28 22:34:12',3000.00,'OK'),(145,18,15,1,1,'2026-01-28 22:34:50',3000.00,'OK'),(146,18,15,1,1,'2026-01-28 22:42:31',3000.00,'OK'),(147,18,15,1,1,'2026-01-28 22:43:09',3000.00,'OK'),(148,18,15,1,1,'2026-01-28 22:43:43',3000.00,'OK'),(149,18,15,1,1,'2026-01-28 22:44:33',3000.00,'OK'),(150,18,15,1,NULL,'2026-01-28 23:14:10',3000.00,'OK'),(151,18,15,1,NULL,'2026-01-28 23:18:28',3000.00,'OK'),(152,18,15,1,1,'2026-01-28 23:20:36',3000.00,'OK'),(153,18,15,1,NULL,'2026-01-28 23:21:40',3000.00,'OK'),(154,19,16,5,1,'2026-01-30 16:07:17',10000.00,'OK'),(155,19,16,1,2,'2026-01-30 16:09:01',10000.00,'OK'),(156,19,16,1,NULL,'2026-01-30 16:09:31',10000.00,'OK');
/*!40000 ALTER TABLE `ventas_entradas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas_entradas_detalle`
--

DROP TABLE IF EXISTS `ventas_entradas_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas_entradas_detalle` (
  `iddetalle` int NOT NULL AUTO_INCREMENT,
  `idventa` int NOT NULL,
  `idsector` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  PRIMARY KEY (`iddetalle`),
  KEY `idventa` (`idventa`),
  KEY `idsector` (`idsector`),
  CONSTRAINT `ventas_entradas_detalle_ibfk_1` FOREIGN KEY (`idventa`) REFERENCES `ventas_entradas` (`idventa`),
  CONSTRAINT `ventas_entradas_detalle_ibfk_2` FOREIGN KEY (`idsector`) REFERENCES `sectores_entradas` (`idsector`)
) ENGINE=InnoDB AUTO_INCREMENT=154 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas_entradas_detalle`
--

LOCK TABLES `ventas_entradas_detalle` WRITE;
/*!40000 ALTER TABLE `ventas_entradas_detalle` DISABLE KEYS */;
INSERT INTO `ventas_entradas_detalle` VALUES (1,4,2,1,6000.00,6000.00),(2,5,1,1,3000.00,3000.00),(3,6,1,1,3000.00,3000.00),(4,7,1,1,3000.00,3000.00),(5,8,3,1,4500.00,4500.00),(6,9,3,1,4500.00,4500.00),(7,10,3,1,4500.00,4500.00),(8,11,1,1,3000.00,3000.00),(9,12,1,1,3000.00,3000.00),(10,13,2,1,6000.00,6000.00),(11,14,1,1,3000.00,3000.00),(12,15,1,1,3000.00,3000.00),(13,16,1,1,3000.00,3000.00),(14,17,1,1,3000.00,3000.00),(15,18,3,1,4500.00,4500.00),(16,19,3,1,4500.00,4500.00),(17,20,1,1,3000.00,3000.00),(18,21,3,1,4500.00,4500.00),(19,22,2,1,6000.00,6000.00),(20,23,1,1,3000.00,3000.00),(21,24,1,1,3000.00,3000.00),(22,25,1,1,3000.00,3000.00),(23,26,1,1,3000.00,3000.00),(24,27,1,1,3000.00,3000.00),(25,28,1,1,3000.00,3000.00),(26,29,1,1,3000.00,3000.00),(27,30,1,1,3000.00,3000.00),(28,31,1,1,3000.00,3000.00),(29,32,1,1,3000.00,3000.00),(30,33,1,1,3000.00,3000.00),(31,34,1,1,3000.00,3000.00),(32,35,1,1,3000.00,3000.00),(33,36,1,1,3000.00,3000.00),(34,37,1,1,3000.00,3000.00),(35,38,1,1,3000.00,3000.00),(36,39,1,1,3000.00,3000.00),(37,40,1,1,3000.00,3000.00),(38,41,1,1,3000.00,3000.00),(39,42,1,1,3000.00,3000.00),(40,43,1,1,3000.00,3000.00),(41,44,1,1,3000.00,3000.00),(42,45,1,1,3000.00,3000.00),(43,46,1,1,3000.00,3000.00),(44,47,1,1,3000.00,3000.00),(45,48,1,1,3000.00,3000.00),(46,49,1,1,3000.00,3000.00),(47,50,1,1,3000.00,3000.00),(48,51,1,1,3000.00,3000.00),(49,52,1,1,3000.00,3000.00),(50,53,1,1,3000.00,3000.00),(51,54,1,1,3000.00,3000.00),(52,55,1,1,3000.00,3000.00),(53,56,1,1,3000.00,3000.00),(54,57,1,1,3000.00,3000.00),(55,58,1,1,3000.00,3000.00),(56,59,1,1,3000.00,3000.00),(57,60,1,1,3000.00,3000.00),(58,61,1,1,3000.00,3000.00),(59,62,1,1,3000.00,3000.00),(60,63,1,1,3000.00,3000.00),(61,64,1,1,3000.00,3000.00),(62,65,1,1,3000.00,3000.00),(63,66,1,1,3000.00,3000.00),(64,67,1,1,3000.00,3000.00),(65,68,1,1,3000.00,3000.00),(66,69,1,1,3000.00,3000.00),(67,70,1,1,3000.00,3000.00),(68,71,1,1,3000.00,3000.00),(69,72,1,1,3000.00,3000.00),(70,73,1,1,3000.00,3000.00),(71,74,1,1,3000.00,3000.00),(72,75,1,1,3000.00,3000.00),(73,76,1,1,3000.00,3000.00),(74,77,1,1,3000.00,3000.00),(75,78,1,1,3000.00,3000.00),(76,79,1,1,3000.00,3000.00),(77,80,1,1,3000.00,3000.00),(78,81,1,1,3000.00,3000.00),(79,82,1,1,3000.00,3000.00),(80,83,1,1,3000.00,3000.00),(81,84,1,1,3000.00,3000.00),(82,85,1,1,3000.00,3000.00),(83,86,1,1,3000.00,3000.00),(84,87,1,1,3000.00,3000.00),(85,88,1,1,3000.00,3000.00),(86,89,1,1,3000.00,3000.00),(87,90,1,1,3000.00,3000.00),(88,91,1,1,3000.00,3000.00),(89,92,1,1,3000.00,3000.00),(90,93,1,1,3000.00,3000.00),(91,94,1,1,3000.00,3000.00),(92,95,1,1,3000.00,3000.00),(93,96,1,1,3000.00,3000.00),(94,97,1,1,3000.00,3000.00),(95,98,1,1,3000.00,3000.00),(96,99,1,1,3000.00,3000.00),(97,100,1,1,3000.00,3000.00),(98,101,1,1,3000.00,3000.00),(99,102,1,1,3000.00,3000.00),(100,103,1,1,3000.00,3000.00),(101,104,1,1,3000.00,3000.00),(102,105,1,1,3000.00,3000.00),(103,106,1,1,3000.00,3000.00),(104,107,1,1,3000.00,3000.00),(105,108,1,1,3000.00,3000.00),(106,109,1,1,3000.00,3000.00),(107,110,1,1,3000.00,3000.00),(108,111,1,1,3000.00,3000.00),(109,112,1,1,3000.00,3000.00),(110,113,1,1,3000.00,3000.00),(111,114,1,1,3000.00,3000.00),(112,115,1,1,3000.00,3000.00),(113,116,1,1,3000.00,3000.00),(114,117,1,1,3000.00,3000.00),(115,118,1,1,3000.00,3000.00),(116,119,1,1,3000.00,3000.00),(117,121,1,1,3000.00,3000.00),(118,120,1,1,3000.00,3000.00),(119,122,1,1,3000.00,3000.00),(120,123,1,1,3000.00,3000.00),(121,124,1,1,3000.00,3000.00),(122,125,1,1,3000.00,3000.00),(123,126,1,1,3000.00,3000.00),(124,127,1,1,3000.00,3000.00),(125,128,1,1,3000.00,3000.00),(126,129,1,1,3000.00,3000.00),(127,130,1,1,3000.00,3000.00),(128,131,1,1,3000.00,3000.00),(129,132,1,1,3000.00,3000.00),(130,133,1,1,3000.00,3000.00),(131,134,1,1,3000.00,3000.00),(132,135,1,1,3000.00,3000.00),(133,136,1,1,3000.00,3000.00),(134,137,1,1,3000.00,3000.00),(135,138,1,1,3000.00,3000.00),(136,139,1,1,3000.00,3000.00),(137,140,1,1,3000.00,3000.00),(138,141,1,1,3000.00,3000.00),(139,142,1,1,3000.00,3000.00),(140,143,1,1,3000.00,3000.00),(141,144,1,1,3000.00,3000.00),(142,145,1,1,3000.00,3000.00),(143,146,1,1,3000.00,3000.00),(144,147,1,1,3000.00,3000.00),(145,148,1,1,3000.00,3000.00),(146,149,1,1,3000.00,3000.00),(147,150,1,1,3000.00,3000.00),(148,151,1,1,3000.00,3000.00),(149,152,1,1,3000.00,3000.00),(150,153,1,1,3000.00,3000.00),(151,154,1,1,10000.00,10000.00),(152,155,1,1,10000.00,10000.00),(153,156,1,1,10000.00,10000.00);
/*!40000 ALTER TABLE `ventas_entradas_detalle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas_entradas_pagos`
--

DROP TABLE IF EXISTS `ventas_entradas_pagos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas_entradas_pagos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idventa` int NOT NULL,
  `idmodopago` int NOT NULL,
  `importe` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idventa` (`idventa`),
  CONSTRAINT `ventas_entradas_pagos_ibfk_1` FOREIGN KEY (`idventa`) REFERENCES `ventas_entradas` (`idventa`)
) ENGINE=InnoDB AUTO_INCREMENT=147 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas_entradas_pagos`
--

LOCK TABLES `ventas_entradas_pagos` WRITE;
/*!40000 ALTER TABLE `ventas_entradas_pagos` DISABLE KEYS */;
INSERT INTO `ventas_entradas_pagos` VALUES (1,30,1,3000.00),(2,31,1,3000.00),(3,32,1,3000.00),(4,33,1,1500.00),(5,33,2,1500.00),(6,34,1,1500.00),(7,34,2,1500.00),(8,35,1,3000.00),(9,36,1,3000.00),(10,37,1,3000.00),(11,38,1,3000.00),(12,39,1,3000.00),(13,40,1,3000.00),(14,41,1,3000.00),(15,42,1,3000.00),(16,43,1,1800.00),(17,44,1,1800.00),(18,43,2,1200.00),(19,44,2,1200.00),(20,45,1,3000.00),(21,46,1,3000.00),(22,47,1,3000.00),(23,48,1,3000.00),(24,49,1,3000.00),(25,50,1,3000.00),(26,51,1,1500.00),(27,51,2,1500.00),(28,52,1,1500.00),(29,52,2,1500.00),(30,53,1,3000.00),(31,54,1,3000.00),(32,55,1,3000.00),(33,56,1,3000.00),(34,57,1,3000.00),(35,58,1,3000.00),(36,59,1,3000.00),(37,60,1,3000.00),(38,61,1,3000.00),(39,62,1,1500.00),(40,63,1,1500.00),(41,62,1,1500.00),(42,63,1,1500.00),(43,64,1,3000.00),(44,65,1,1500.00),(45,65,3,1500.00),(46,66,1,1500.00),(47,66,3,1500.00),(48,67,1,3000.00),(49,68,1,1500.00),(50,68,2,1500.00),(51,69,1,1500.00),(52,69,2,1500.00),(53,70,1,3000.00),(54,81,1,3000.00),(55,82,1,3000.00),(56,83,1,3000.00),(57,84,1,1500.00),(58,84,2,1500.00),(59,85,1,1500.00),(60,85,2,1500.00),(61,86,1,3000.00),(62,87,1,3000.00),(63,88,1,1500.00),(64,89,1,1500.00),(65,88,2,1500.00),(66,89,2,1500.00),(67,90,1,3000.00),(68,91,1,3000.00),(69,92,1,3000.00),(70,93,1,3000.00),(71,94,1,1500.00),(72,94,2,1500.00),(73,95,1,1500.00),(74,95,2,1500.00),(75,96,1,3000.00),(76,97,1,3000.00),(77,98,1,3000.00),(78,99,1,3000.00),(79,100,1,3000.00),(80,101,1,3000.00),(81,102,1,1500.00),(82,102,2,1500.00),(83,103,1,1500.00),(84,103,2,1500.00),(85,104,1,3000.00),(86,105,1,3000.00),(87,106,1,1500.00),(88,106,2,1500.00),(89,107,1,1500.00),(90,107,2,1500.00),(91,108,1,3000.00),(92,109,1,3000.00),(93,110,1,3000.00),(94,111,1,3000.00),(95,112,1,3000.00),(96,113,1,3000.00),(97,114,1,3000.00),(98,115,1,3000.00),(99,116,1,3000.00),(100,117,1,3000.00),(101,118,1,3000.00),(102,119,1,3000.00),(103,121,1,3000.00),(104,120,1,3000.00),(105,122,1,3000.00),(106,123,1,3000.00),(107,124,1,3000.00),(108,125,1,3000.00),(109,126,1,3000.00),(110,127,1,3000.00),(111,128,1,3000.00),(112,129,1,3000.00),(113,130,1,1500.00),(114,130,2,1500.00),(115,131,1,1500.00),(116,131,2,1500.00),(117,132,1,3000.00),(118,133,1,3000.00),(119,134,1,3000.00),(120,135,1,3000.00),(121,136,1,3000.00),(122,137,1,3000.00),(123,138,1,3000.00),(124,139,1,3000.00),(125,140,1,3000.00),(126,141,1,3000.00),(127,142,1,3000.00),(128,143,1,3000.00),(129,144,1,1800.00),(130,144,2,1200.00),(131,145,1,3000.00),(132,146,1,3000.00),(133,147,1,3000.00),(134,148,1,3000.00),(135,149,1,3000.00),(136,150,1,1500.00),(137,150,2,1500.00),(138,151,1,1500.00),(139,151,3,1500.00),(140,152,1,3000.00),(141,153,1,1900.00),(142,153,3,1100.00),(143,154,1,10000.00),(144,155,2,10000.00),(145,156,1,7000.00),(146,156,2,3000.00);
/*!40000 ALTER TABLE `ventas_entradas_pagos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas_pagos`
--

DROP TABLE IF EXISTS `ventas_pagos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas_pagos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idventa` int NOT NULL,
  `idmodopago` int NOT NULL,
  `importe` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_vp_venta` (`idventa`),
  KEY `fk_vp_modopago` (`idmodopago`),
  CONSTRAINT `fk_vp_modopago` FOREIGN KEY (`idmodopago`) REFERENCES `modopago` (`idmodopago`),
  CONSTRAINT `fk_vp_venta` FOREIGN KEY (`idventa`) REFERENCES `ventas` (`idventa`)
) ENGINE=InnoDB AUTO_INCREMENT=119 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas_pagos`
--

LOCK TABLES `ventas_pagos` WRITE;
/*!40000 ALTER TABLE `ventas_pagos` DISABLE KEYS */;
INSERT INTO `ventas_pagos` VALUES (1,133,1,20000.00),(2,134,2,8000.00),(3,135,3,14000.00),(4,136,3,12000.00),(5,137,3,14000.00),(6,138,3,15000.00),(7,139,3,17000.00),(8,140,1,20000.00),(9,141,1,8000.00),(10,142,1,5000.00),(11,143,3,14000.00),(12,144,1,8000.00),(13,145,3,20000.00),(14,146,3,20000.00),(15,147,3,17000.00),(16,148,1,8000.00),(17,149,1,7000.00),(18,150,1,26000.00),(19,151,1,8000.00),(20,152,3,12000.00),(21,153,1,8000.00),(22,154,3,17000.00),(23,155,3,26000.00),(24,156,3,28000.00),(25,157,3,15000.00),(26,158,3,9000.00),(27,159,3,9000.00),(28,160,1,20000.00),(29,161,1,8000.00),(30,162,1,8000.00),(31,163,3,15000.00),(32,164,1,8000.00),(33,165,1,7000.00),(34,165,2,8000.00),(35,166,1,7000.00),(36,167,2,8000.00),(37,168,1,5000.00),(38,168,2,3000.00),(39,169,1,7000.00),(40,170,2,20000.00),(41,171,1,8000.00),(42,172,1,3000.00),(43,172,2,4000.00),(44,173,1,0.00),(45,174,1,7000.00),(46,175,1,5000.00),(47,176,1,15000.00),(48,176,2,5000.00),(49,177,1,5000.00),(50,177,2,3000.00),(51,178,1,5000.00),(52,179,1,0.00),(53,180,1,0.00),(54,181,1,7000.00),(55,182,1,4000.00),(56,182,3,4000.00),(57,183,1,33000.00),(58,184,1,18000.00),(59,185,1,6000.00),(60,186,1,10000.00),(61,186,2,8000.00),(62,187,1,8000.00),(63,188,1,7000.00),(64,189,1,46000.00),(65,190,1,19000.00),(66,191,1,9000.00),(67,191,2,9000.00),(68,192,1,0.00),(69,193,1,7000.00),(70,194,1,9000.00),(72,196,1,5000.00),(73,197,1,7000.00),(80,204,1,5000.00),(81,205,1,7000.00),(82,206,1,7000.00),(83,207,1,7000.00),(84,208,1,7000.00),(85,209,1,5000.00),(86,210,1,7000.00),(87,211,1,5000.00),(88,212,1,10000.00),(89,213,1,10000.00),(90,214,1,5000.00),(91,215,1,7000.00),(92,216,1,7000.00),(93,217,1,3000.00),(94,217,2,2000.00),(95,218,1,10000.00),(96,219,1,30000.00),(97,220,1,5000.00),(98,221,1,5000.00),(99,222,1,10000.00),(100,223,1,5000.00),(101,224,1,5000.00),(102,225,1,5000.00),(103,226,1,10000.00),(104,227,1,5000.00),(105,228,1,5000.00),(106,229,1,5000.00),(107,230,1,5000.00),(108,231,1,5000.00),(109,232,1,5000.00),(110,233,1,10000.00),(111,234,1,5000.00),(112,235,1,5000.00),(113,236,1,5000.00),(114,237,1,5000.00),(115,238,1,5000.00),(116,239,1,5000.00),(117,240,1,10000.00),(118,241,1,5000.00);
/*!40000 ALTER TABLE `ventas_pagos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-24 10:42:42
