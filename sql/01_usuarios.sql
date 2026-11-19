USE techandes;

CREATE TABLE IF NOT EXISTS usuarios (
  id_usuario INT NOT NULL AUTO_INCREMENT,
  usuario VARCHAR(30) NOT NULL,
  clave_hash VARCHAR(255) NOT NULL,
  rol VARCHAR(15) NOT NULL DEFAULT 'VENDEDOR',
  id_empleado INT NOT NULL,
  activo TINYINT NOT NULL DEFAULT 1,
  ultimo_acceso DATETIME NULL,
  CONSTRAINT pk_usuarios PRIMARY KEY (id_usuario),
  CONSTRAINT uq_usuarios_usuario UNIQUE (usuario),
  CONSTRAINT uq_usuarios_empleado UNIQUE (id_empleado),
  CONSTRAINT fk_usuarios_empleados FOREIGN KEY (id_empleado)
    REFERENCES empleados (id_empleado)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT ck_usuarios_rol CHECK (rol IN ('ADMIN', 'VENDEDOR')),
  CONSTRAINT ck_usuarios_activo CHECK (activo IN (0, 1))
) ENGINE = InnoDB;

-- Hashes scrypt de Admin2026* (ADMIN) y Ventas2026* (VENDEDOR).
-- Los id_empleado siguen el orden del taller: 1 mprieto ... 8 fcuellar.
-- Este INSERT exige que esos 8 empleados ya existan.
INSERT INTO usuarios (usuario, clave_hash, rol, id_empleado) VALUES
('mprieto', 'scrypt:32768:8:1$ThOe4AddZzpZy0Du$70fad18e9cd4df17732f830fd03806cb3e4bbcd482bb5fa54cacdcd91d821c565fe51bfda9056d79c40f5465134bf7f9d57108da1cdebec99dfa3a4956da03a5', 'ADMIN', 1),
('hbustos', 'scrypt:32768:8:1$ThOe4AddZzpZy0Du$70fad18e9cd4df17732f830fd03806cb3e4bbcd482bb5fa54cacdcd91d821c565fe51bfda9056d79c40f5465134bf7f9d57108da1cdebec99dfa3a4956da03a5', 'ADMIN', 2),
('crobayo', 'scrypt:32768:8:1$ThOe4AddZzpZy0Du$70fad18e9cd4df17732f830fd03806cb3e4bbcd482bb5fa54cacdcd91d821c565fe51bfda9056d79c40f5465134bf7f9d57108da1cdebec99dfa3a4956da03a5', 'ADMIN', 3),
('klozada', 'scrypt:32768:8:1$qtZTAiyylKTL0KFK$c5d2fca1d46b097e326c321b492e638ad262f3dfb94cd81b2683adab170a9ce791d1beead9095f9ed8d2b5fd17d23f86f91dfc0770b0b7e6e7b0687a926f4b34', 'VENDEDOR', 4),
('ytafur', 'scrypt:32768:8:1$qtZTAiyylKTL0KFK$c5d2fca1d46b097e326c321b492e638ad262f3dfb94cd81b2683adab170a9ce791d1beead9095f9ed8d2b5fd17d23f86f91dfc0770b0b7e6e7b0687a926f4b34', 'VENDEDOR', 5),
('boviedo', 'scrypt:32768:8:1$qtZTAiyylKTL0KFK$c5d2fca1d46b097e326c321b492e638ad262f3dfb94cd81b2683adab170a9ce791d1beead9095f9ed8d2b5fd17d23f86f91dfc0770b0b7e6e7b0687a926f4b34', 'VENDEDOR', 6),
('lmurcia', 'scrypt:32768:8:1$qtZTAiyylKTL0KFK$c5d2fca1d46b097e326c321b492e638ad262f3dfb94cd81b2683adab170a9ce791d1beead9095f9ed8d2b5fd17d23f86f91dfc0770b0b7e6e7b0687a926f4b34', 'VENDEDOR', 7),
('fcuellar', 'scrypt:32768:8:1$qtZTAiyylKTL0KFK$c5d2fca1d46b097e326c321b492e638ad262f3dfb94cd81b2683adab170a9ce791d1beead9095f9ed8d2b5fd17d23f86f91dfc0770b0b7e6e7b0687a926f4b34', 'VENDEDOR', 8);

SELECT u.usuario, u.rol, e.id_empleado,
       CONCAT(e.nombre, ' ', e.apellidos) AS empleado, e.cargo
FROM usuarios u
JOIN empleados e ON e.id_empleado = u.id_empleado
ORDER BY u.id_usuario;




SELECT u.usuario, u.rol, e.id_empleado,
       CONCAT(e.nombres, ' ', e.apellidos) AS empleado, e.cargo
FROM usuarios u
JOIN empleados e ON e.id_empleado = u.id_empleado
ORDER BY u.id_usuario;

DESCRIBE empleados;



USE TecHandes;

DESCRIBE clientes;
