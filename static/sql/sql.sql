mysql -u root -p

CREATE DATABASE `Financiera`;

USE `Financiera`;

DROP TABLE IF EXISTS `Financiera`.`usuario`;

CREATE TABLE `Financiera`.`usuario` (
  `usu_id` BIGINT UNIQUE AUTO_INCREMENT,
  `usu_nombre` VARCHAR(45) NULL,
  `usu_email` VARCHAR(45) NULL,
  `usu_pass` VARCHAR(255) NULL,
  PRIMARY KEY (`usu_id`));

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `Financiera`.`crearUsuario`(
    IN p_nombre VARCHAR(45),
    IN p_email VARCHAR(45),
    IN p_pass VARCHAR(255)
)
BEGIN
    if ( select exists (select 1 from usuario where usu_nombre = p_nombre) ) THEN     
        select 'Usuario ya Existe!';     
    ELSE     
        insert into tbl_user
        (
            usu_nombre,
            usu_email,
            usu_pass
        )
        values
        (
            p_nombre,
            p_email,
            p_pass
        );
     
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `Financiera`.`validarLogin`(
IN p_usu VARCHAR(45)
)
BEGIN
    select * from usuario where usu_nombre = p_usu;
END$$
DELIMITER ;

DROP TABLE IF EXISTS `Financiera`.`financiacion`;

CREATE TABLE `Financiera`.`financiacion` (
  `fin_id` int(11) NOT NULL AUTO_INCREMENT,
  `fin_importe` float(11,2) DEFAULT NULL,
  `fin_veces` int(3) DEFAULT NULL,
  `fin_prestacion` float(11,2) DEFAULT NULL,
  `fin_fecha_ini` datetime DEFAULT NULL,
  `fin_mes_actual` int(3) DEFAULT NULL,
  `fin_mes_pagado` int(3) DEFAULT NULL,
  `fin_meses_retraso` int(3) DEFAULT NULL,
  `fin_importe_retraso` float(11,2) DEFAULT NULL,
  `fin_usu_id` int(11),
  PRIMARY KEY (`fin_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

DROP procedure IF EXISTS `getFin`;
 
DELIMITER $$

CREATE PROCEDURE `getFin` (
IN p_usu_id int(11)
)
BEGIN
    select * from financiacion where fin_usu_id = p_usu_id;
END$$
 
DELIMITER ;

DROP TABLE IF EXISTS `Financiera`.`solicitud`;

CREATE TABLE `Financiera`.`solicitud` (
  `sol_id` int(11) NOT NULL AUTO_INCREMENT,
  `sol_importe` float(11,2) DEFAULT NULL,
  `sol_veces` int(3) DEFAULT NULL,
  `sol_date` DATE DEFAULT NULL,
  `sol_usu_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`sol_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

DROP procedure IF EXISTS `Financiera`.`addSolicitud`;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `Financiera`.`addSolicitud`(
    IN p_valor float(11,2),
    IN p_meses int(3),
    IN p_usu_id int(11)
)
BEGIN
    insert into solicitud(
        sol_importe,
        sol_veces,
        sol_usu_id,
        sol_date
    )
    values
    (
        p_valor,
        p_meses,
        p_usu_id,
        NOW()
    );
END$$ 

DELIMITER ;

INSERT INTO financiera.financiacion (fin_importe, fin_veces, fin_prestacion, fin_fecha_ini, fin_mes_actual, fin_mes_pagado, fin_meses_retraso, fin_importe_retraso, fin_usu_id)
VALUES (3000, 15, 220, '2019-10-01', 11, 11, 0, 0, 2),
(350.99, 2, 165.55, '2019-11-01', 1, 1, 0, 0, 2),
(1100.50, 9, 220.20, '2019-04-01', 7, 5, 2, 455.50, 2),
(990.99, 15, 220.99, '2019-10-01', 11, 11, 0, 0, 2),
(4555.55, 10, 420.50, '2019-06-01', 5, 5, 0, 0, 1),
(805.10, 6, 145.50, '2019-08-01', 3, 1, 2, 305.55, 1),
(1000.00, 10, 110.55, '2019-10-01', 11, 11, 0, 0, 3),
(330.30, 2, 155.55, '2019-11-01', 1, 1, 0, 0, 3),
(1010.50, 9, 220.10, '2019-04-01', 7, 5, 2, 455.99, 4),
(4000, 10, 420.20, '2019-06-01', 5, 5, 0, 0, 5),
(829.99, 6, 145.50, '2019-08-01', 3, 1, 2, 310.20, 6);


DROP TABLE IF EXISTS `Financiera`.`inversiones`;

CREATE TABLE `Financiera`.`inversiones` (
  `inv_id` int(11) NOT NULL AUTO_INCREMENT,
  `inv_producto` int(11) NULL,
  `inv_importe` float(11,2) DEFAULT NULL,
  `inv_date` DATE DEFAULT NULL,
  `inv_usu_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`inv_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

USE `Financiera`;
DROP procedure IF EXISTS `Financiera`.`getInver`;
 
DELIMITER $$
CREATE PROCEDURE `Financiera`.`getInver` (
IN p_usu_id int(11)
)
BEGIN
    select * from inversiones where inv_usu_id = p_usu_id;
END$$
 
DELIMITER ;

INSERT INTO financiera.inversiones (inv_producto, inv_importe, inv_date, inv_usu_id)
VALUES (1, 2500, '2018-12-01', 2),
(2, 430, '2018-10-01', 2),
(3, 1250, '2018-08-01', 2),
(4, 810, '2018-07-01', 2),
(1, 725, '2018-06-01', 1),
(3, 3330, '2018-10-01', 1),
(4, 5200, '2018-12-01', 1),
(2, 900, '2018-06-01', 3),
(4, 7050, '2018-05-01', 3),
(1, 430, '2018-04-01', 4),
(3, 970, '2018-03-01', 4),
(3, 5000, '2018-08-01', 5),
(4, 7000, '2018-02-01', 6),
(1, 8000, '2018-07-01', 7),
(2, 10000, '2018-09-01', 8);

