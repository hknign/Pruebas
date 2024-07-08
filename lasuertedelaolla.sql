-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 07-07-2024 a las 19:58:41
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `lasuertedelaolla`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administrador`
--

CREATE TABLE `administrador` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  `correo` varchar(50) DEFAULT NULL,
  `telefono` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `administrador`
--

INSERT INTO `administrador` (`id`, `nombre`, `apellido`, `correo`, `telefono`) VALUES
(1, 'Laura', 'Gomez', 'laura.gomez@gmail.com', '987654321'),
(2, 'Carlos', 'Perez', 'carlos.perez@hotmail.com', '987654321');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `correo` varchar(50) DEFAULT NULL,
  `telefono` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`id`, `nombre`, `correo`, `telefono`) VALUES
(1, 'Ana Lopez', 'ana.lopez@example.com', '987551234'),
(2, 'Luis Torres', 'luis.torres@example.com', '975555678'),
(3, 'Sofia Martinez', 'sofia.martinez@example.com', '955508765'),
(5, 'pablito', 'pablo@gmail.com', '974327479');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comentarios`
--

CREATE TABLE `comentarios` (
  `id` int(11) NOT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `comentario` varchar(255) DEFAULT NULL,
  `valoracion` int(11) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `comentarios`
--

INSERT INTO `comentarios` (`id`, `id_cliente`, `id_producto`, `comentario`, `valoracion`, `fecha`) VALUES
(1, 1, 1, 'Muy buena', 5, '2024-05-01 12:00:00'),
(2, 2, 2, 'Deliciosa', 4, '2024-05-02 13:00:00'),
(3, 3, 3, 'Excelente', 5, '2024-05-03 14:00:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalles_pedido`
--

CREATE TABLE `detalles_pedido` (
  `id_pedido` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `comentario` varchar(255) DEFAULT NULL,
  `valoracion` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalles_pedido`
--

INSERT INTO `detalles_pedido` (`id_pedido`, `id_producto`, `cantidad`, `comentario`, `valoracion`) VALUES
(1, 1, 2, 'Sin cebolla', 5),
(1, 3, 1, 'Con salsa picante', 5),
(2, 2, 1, 'Extra queso', 4),
(3, 1, 1, 'Normal', 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalles_venta`
--

CREATE TABLE `detalles_venta` (
  `id_venta` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `precio_unitario` float DEFAULT NULL,
  `promocion_aplicada` varchar(100) DEFAULT NULL,
  `descuento` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalles_venta`
--

INSERT INTO `detalles_venta` (`id_venta`, `id_producto`, `cantidad`, `precio_unitario`, `promocion_aplicada`, `descuento`) VALUES
(1, 1, 2, 4500, 'Promo Hamburguesa', 900.00),
(1, 3, 1, 2200, 'Promo Tacos', 220.00),
(2, 2, 1, 6800, 'Promo Pizza', 1020.00),
(3, 1, 1, 4500, 'Promo Hamburguesa', 900.00),
(3, 2, 3, 6800, 'Promo Pizza', 1020.00),
(10, 2, 1, 6800, NULL, NULL),
(13, 1, 1, 4500, NULL, NULL),
(13, 2, 1, 6800, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado`
--

CREATE TABLE `empleado` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  `correo` varchar(50) DEFAULT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `id_usuario` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `empleado`
--

INSERT INTO `empleado` (`id`, `nombre`, `apellido`, `correo`, `telefono`, `id_usuario`) VALUES
(2, 'Ana', 'Martinez', 'ana.martinez@example.com', '987654321', 2),
(3, 'Pedro', 'Garcia', 'pedro.garcia@example.com', '987654321', 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entregas_a_domicilio`
--

CREATE TABLE `entregas_a_domicilio` (
  `id` int(11) NOT NULL,
  `id_pedido` int(11) DEFAULT NULL,
  `id_repartidor` int(11) DEFAULT NULL,
  `direccion` varchar(255) NOT NULL,
  `ciudad` varchar(50) NOT NULL,
  `estado` enum('PENDIENTE','ENTREGADO','NO ENTREGADO') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `entregas_a_domicilio`
--

INSERT INTO `entregas_a_domicilio` (`id`, `id_pedido`, `id_repartidor`, `direccion`, `ciudad`, `estado`) VALUES
(1, 1, 1, 'Calle 123', 'Ciudad A', 'ENTREGADO'),
(2, 2, 2, 'Avenida 456', 'Ciudad B', 'PENDIENTE'),
(3, 3, 1, 'Boulevard 789', 'Ciudad C', 'NO ENTREGADO');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `informacion_nutricional`
--

CREATE TABLE `informacion_nutricional` (
  `id` int(11) NOT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `calorias` int(11) DEFAULT NULL,
  `grasas_totales` decimal(5,2) DEFAULT NULL,
  `proteinas` decimal(5,2) DEFAULT NULL,
  `carbohidratos` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `informacion_nutricional`
--

INSERT INTO `informacion_nutricional` (`id`, `id_producto`, `calorias`, `grasas_totales`, `proteinas`, `carbohidratos`) VALUES
(1, 1, 550, 35.00, 25.00, 45.00),
(2, 2, 800, 40.00, 35.00, 90.00),
(3, 3, 250, 15.00, 10.00, 20.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `informes_diarios`
--

CREATE TABLE `informes_diarios` (
  `id` int(11) NOT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `cantidad_total_productos_vendidos` int(11) DEFAULT NULL,
  `total_venta` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `informes_diarios`
--

INSERT INTO `informes_diarios` (`id`, `fecha_inicio`, `fecha_fin`, `cantidad_total_productos_vendidos`, `total_venta`) VALUES
(1, '2024-05-01', '2024-05-01', 5, 9000.00),
(2, '2024-05-02', '2024-05-02', 7, 6800.00),
(3, '2024-05-03', '2024-05-03', 10, 2200.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `informes_mensuales`
--

CREATE TABLE `informes_mensuales` (
  `id` int(11) NOT NULL,
  `mes` int(11) NOT NULL,
  `año` int(11) NOT NULL,
  `cantidad_total_productos_vendidos` int(11) DEFAULT NULL,
  `total_venta` decimal(10,2) DEFAULT NULL
) ;

--
-- Volcado de datos para la tabla `informes_mensuales`
--

INSERT INTO `informes_mensuales` (`id`, `mes`, `año`, `cantidad_total_productos_vendidos`, `total_venta`) VALUES
(1, 5, 2024, 1000, 5990.00),
(2, 6, 2024, 1200, 7188.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario`
--

CREATE TABLE `inventario` (
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `ultima_actualizacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inventario`
--

INSERT INTO `inventario` (`id_producto`, `cantidad`, `ultima_actualizacion`) VALUES
(1, 47, '2024-05-04 10:00:00'),
(2, 29, '2024-05-04 10:00:00'),
(3, 99, '2024-05-04 10:00:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `menus_especiales`
--

CREATE TABLE `menus_especiales` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `menus_especiales`
--

INSERT INTO `menus_especiales` (`id`, `nombre`, `descripcion`, `fecha_inicio`, `fecha_fin`) VALUES
(1, 'Menu de Navidad', 'Menu especial para Navidad', '2024-12-01', '2024-12-25'),
(2, 'Menu de Año Nuevo', 'Menu especial para Año Nuevo', '2024-12-26', '2025-01-01'),
(4, 'menu niños', 'especial dia del niño ', '2024-08-01', '2024-08-06');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mesa`
--

CREATE TABLE `mesa` (
  `id` int(11) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `capacidad` int(11) NOT NULL,
  `estado` enum('reservado','libre') NOT NULL DEFAULT 'libre'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mesa`
--

INSERT INTO `mesa` (`id`, `descripcion`, `capacidad`, `estado`) VALUES
(1, 'Mesa para 4 personas', 4, 'libre'),
(2, 'Mesa para 2 personas', 2, 'libre'),
(3, 'Mesa para 6 personas', 6, 'libre'),
(6, 'mesa para 8', 8, 'libre');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notificacion_promocion`
--

CREATE TABLE `notificacion_promocion` (
  `id` int(11) NOT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `id_promocion` int(11) DEFAULT NULL,
  `fecha_envio` datetime DEFAULT NULL,
  `leido` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `notificacion_promocion`
--

INSERT INTO `notificacion_promocion` (`id`, `id_cliente`, `id_promocion`, `fecha_envio`, `leido`) VALUES
(1, 1, 1, '2024-05-01 08:00:00', 1),
(2, 2, 2, '2024-05-02 08:00:00', 0),
(3, 3, 3, '2024-05-03 08:00:00', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedido`
--

CREATE TABLE `pedido` (
  `id` int(11) NOT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `total` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedido`
--

INSERT INTO `pedido` (`id`, `id_cliente`, `fecha`, `total`) VALUES
(1, 1, '2024-05-01 12:00:00', 9000),
(2, 2, '2024-05-02 13:00:00', 6800),
(3, 3, '2024-05-03 14:00:00', 2200);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `precio` float DEFAULT NULL,
  `cantidad_disponible` int(11) DEFAULT NULL,
  `promocion` tinyint(1) DEFAULT NULL,
  `descuento_promocion` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`id`, `nombre`, `descripcion`, `precio`, `cantidad_disponible`, `promocion`, `descuento_promocion`) VALUES
(1, 'Hamburguesa', 'Hamburguesa de res con queso y tocino', 4500, 50, 1, 20.00),
(2, 'Pizza', 'Pizza de pepperoni con extra queso', 6800, 30, 1, 15.00),
(3, 'Taco', 'Taco de carne asada con guacamole', 2200, 100, 1, 10.00),
(5, 'pollo', 'pollo al horno con verduras', 14122, 2, 0, 0.00),
(6, 'Sándwich de pollo', 'Sándwich de pechuga de pollo con vegetales frescos', 3500, 40, 1, 15.00),
(7, 'Ensalada César', 'Ensalada clásica con pollo a la parrilla y aderezo César', 2800, 25, 1, 10.00),
(8, 'Pasta Carbonara', 'Pasta con salsa cremosa de huevo, panceta y queso parmesano', 5200, 20, 1, 20.00),
(9, 'Sushi Roll Tempura', 'Sushi roll tempura con camarón, aguacate y queso crema', 6200, 30, 1, 15.00),
(10, 'Filete de salmón', 'Filete de salmón a la parrilla con vegetales al vapor', 7800, 15, 1, 10.00),
(11, 'Wrap de vegetales', 'Wrap de tortilla de harina relleno de vegetales frescos', 2900, 35, 1, 0.00),
(12, 'Lasagna Bolognesa', 'Lasagna tradicional con carne molida, salsa de tomate y queso', 6400, 20, 1, 25.00),
(13, 'Tarta de manzana', 'Tarta casera de manzana con masa crujiente y relleno de canela', 3800, 25, 1, 10.00),
(14, 'Ceviche de camarón', 'Ceviche fresco de camarón con limón, cilantro y cebolla morada', 4200, 20, 1, 0.00),
(15, 'Burrito de carne', 'Burrito grande de carne de res con frijoles y salsa picante', 3500, 30, 1, 15.00),
(16, 'Pastel de chocolate', 'Pastel de chocolate oscuro con cobertura de ganache', 4500, 15, 1, 20.00),
(17, 'Risotto de champiñones', 'Risotto cremoso con champiñones y queso parmesano', 5800, 25, 1, 10.00),
(18, 'Empanadas argentinas', 'Empanadas rellenas de carne picada, huevo duro y aceitunas', 3200, 40, 1, 0.00),
(19, 'Cocktail de camarones', 'Cocktail de camarones con salsa de cóctel y aguacate', 4800, 20, 1, 15.00),
(20, 'Tacos dorados', 'Tacos dorados crujientes rellenos de pollo deshebrado', 2900, 30, 1, 10.00),
(21, 'Enchiladas verdes', 'Enchiladas verdes de pollo con salsa verde y queso gratinado', 3900, 25, 1, 0.00),
(22, 'Pizza vegetariana', 'Pizza con vegetales frescos y queso mozzarella', 6000, 20, 1, 15.00),
(23, 'Hot dog clásico', 'Hot dog con salchicha de res, mostaza, ketchup y pepinillos', 2500, 50, 1, 10.00),
(24, 'Pollo al curry', 'Pollo al curry con arroz basmati y verduras salteadas', 6900, 15, 1, 20.00),
(25, 'Huevos rancheros', 'Huevos fritos sobre tortillas de maíz con salsa ranchera y frijoles refritos', 3200, 30, 1, 10.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `promocion`
--

CREATE TABLE `promocion` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `descuento` decimal(5,2) DEFAULT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `promocion`
--

INSERT INTO `promocion` (`id`, `nombre`, `descripcion`, `descuento`, `fecha_inicio`, `fecha_fin`) VALUES
(1, 'Promo Hamburguesa', '20% de descuento en hamburguesas', 20.00, '2024-05-01', '2024-05-07'),
(2, 'Promo Pizza', '15% de descuento en pizzas', 15.00, '2024-05-01', '2024-05-07'),
(3, 'Promo Tacos', '10% de descuento en tacos', 10.00, '2024-05-01', '2024-05-07');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedor`
--

CREATE TABLE `proveedor` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `correo` varchar(50) DEFAULT NULL,
  `telefono` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proveedor`
--

INSERT INTO `proveedor` (`id`, `nombre`, `correo`, `telefono`) VALUES
(1, 'Distribuidora A', 'distribuidoraA@gmail.com', '987654321'),
(2, 'Distribuidora B', 'distribuidoraB@gmail.com', '987654321');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `redes_sociales`
--

CREATE TABLE `redes_sociales` (
  `id` int(11) NOT NULL,
  `plataforma` varchar(50) DEFAULT NULL,
  `enlace` varchar(255) DEFAULT NULL,
  `imagen` blob DEFAULT NULL,
  `imagen_path` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `redes_sociales`
--

INSERT INTO `redes_sociales` (`id`, `plataforma`, `enlace`, `imagen`, `imagen_path`) VALUES
(11, 'wsp', 'https://web.whatsapp.com/', NULL, 'images/wsp.png'),
(12, 'instagram', 'https://www.instagram.com/lasuertedelaolladelivery2.0/', NULL, 'images/instagram.png'),
(16, 'facebook', 'https://www.facebook.com/suertedelaolladelivery', NULL, 'images/facebook.png');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `repartidor`
--

CREATE TABLE `repartidor` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  `correo` varchar(50) DEFAULT NULL,
  `telefono` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `repartidor`
--

INSERT INTO `repartidor` (`id`, `nombre`, `apellido`, `correo`, `telefono`) VALUES
(1, 'Pablo', 'Rodriguez', 'pablo.rodriguez@example.com', '987654321'),
(2, 'Maria', 'Lopez', 'maria.lopez@example.com', '948324827');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reserva`
--

CREATE TABLE `reserva` (
  `id` int(11) NOT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `id_mesa` int(11) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `cantidad_personas` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `reserva`
--

INSERT INTO `reserva` (`id`, `id_cliente`, `id_mesa`, `fecha`, `cantidad_personas`) VALUES
(1, 1, 1, '2024-05-04', 4),
(2, 2, 2, '2024-05-05', 2),
(3, 3, 3, '2024-05-06', 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sesion_cliente`
--

CREATE TABLE `sesion_cliente` (
  `id` int(11) NOT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `inicio_sesion` datetime DEFAULT NULL,
  `fin_sesion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sesion_cliente`
--

INSERT INTO `sesion_cliente` (`id`, `id_cliente`, `inicio_sesion`, `fin_sesion`) VALUES
(1, 1, '2024-05-01 08:00:00', '2024-05-01 09:00:00'),
(2, 2, '2024-05-02 10:00:00', '2024-05-02 11:00:00'),
(3, 3, '2024-05-03 12:00:00', '2024-05-03 13:00:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `rol` varchar(20) DEFAULT NULL,
  `correo` varchar(50) DEFAULT NULL,
  `contraseña` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `nombre`, `rol`, `correo`, `contraseña`) VALUES
(2, 'Maria Gomez', 'Cajero', 'maria.gomez@example.com', 'password'),
(3, 'Carlos Diaz', 'Mesero', 'carlos.diaz@example.com', 'password'),
(5, 'Pepe ', 'Administrador', 'pepito@gmail.com', 'pepe'),
(6, 'sebastian', 'administrador', 'seb@gmail.com', '12345'),
(7, 'pablo', 'Cajero', 'pb@gmail.com', '12345'),
(8, 'admin', 'Administrador', 'eladmin@gmail.com', 'admin'),
(9, 'carlitos', 'Administrador', 'carlitos@gmail.com', '12345'),
(10, 'Manuel', 'Administrador', 'manolito@gmail.com', 'reveco'),
(11, 'ignacio', 'administrador', 'igna@gmail.com', '12345');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `venta`
--

CREATE TABLE `venta` (
  `id` int(11) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `total` float DEFAULT NULL,
  `valor_iva` decimal(10,2) DEFAULT 0.19
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `venta`
--

INSERT INTO `venta` (`id`, `id_usuario`, `id_cliente`, `fecha`, `total`, `valor_iva`) VALUES
(1, 2, 1, '2024-05-01', 17920, 0.19),
(2, 2, 2, '2024-05-02', 8980, 0.19),
(3, 3, 3, '2024-05-03', 5980, 0.19),
(10, 3, 3, '2024-06-03', 9780, 0.19),
(12, 2, 2, '2024-07-08', 12000, 0.19),
(13, NULL, NULL, NULL, 11300, 0.19);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administrador`
--
ALTER TABLE `administrador`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `comentarios`
--
ALTER TABLE `comentarios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `detalles_pedido`
--
ALTER TABLE `detalles_pedido`
  ADD PRIMARY KEY (`id_pedido`,`id_producto`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `detalles_venta`
--
ALTER TABLE `detalles_venta`
  ADD PRIMARY KEY (`id_venta`,`id_producto`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `entregas_a_domicilio`
--
ALTER TABLE `entregas_a_domicilio`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_pedido` (`id_pedido`),
  ADD KEY `id_repartidor` (`id_repartidor`);

--
-- Indices de la tabla `informacion_nutricional`
--
ALTER TABLE `informacion_nutricional`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `informes_diarios`
--
ALTER TABLE `informes_diarios`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `informes_mensuales`
--
ALTER TABLE `informes_mensuales`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD PRIMARY KEY (`id_producto`);

--
-- Indices de la tabla `menus_especiales`
--
ALTER TABLE `menus_especiales`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `mesa`
--
ALTER TABLE `mesa`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `notificacion_promocion`
--
ALTER TABLE `notificacion_promocion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_promocion` (`id_promocion`);

--
-- Indices de la tabla `pedido`
--
ALTER TABLE `pedido`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_cliente` (`id_cliente`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `promocion`
--
ALTER TABLE `promocion`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `redes_sociales`
--
ALTER TABLE `redes_sociales`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `repartidor`
--
ALTER TABLE `repartidor`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `reserva`
--
ALTER TABLE `reserva`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_mesa` (`id_mesa`);

--
-- Indices de la tabla `sesion_cliente`
--
ALTER TABLE `sesion_cliente`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_cliente` (`id_cliente`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `venta`
--
ALTER TABLE `venta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_cliente` (`id_cliente`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `administrador`
--
ALTER TABLE `administrador`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `comentarios`
--
ALTER TABLE `comentarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `empleado`
--
ALTER TABLE `empleado`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `entregas_a_domicilio`
--
ALTER TABLE `entregas_a_domicilio`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `informacion_nutricional`
--
ALTER TABLE `informacion_nutricional`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `informes_diarios`
--
ALTER TABLE `informes_diarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `informes_mensuales`
--
ALTER TABLE `informes_mensuales`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `menus_especiales`
--
ALTER TABLE `menus_especiales`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `mesa`
--
ALTER TABLE `mesa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `notificacion_promocion`
--
ALTER TABLE `notificacion_promocion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `pedido`
--
ALTER TABLE `pedido`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT de la tabla `promocion`
--
ALTER TABLE `promocion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `redes_sociales`
--
ALTER TABLE `redes_sociales`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `repartidor`
--
ALTER TABLE `repartidor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `reserva`
--
ALTER TABLE `reserva`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `sesion_cliente`
--
ALTER TABLE `sesion_cliente`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `venta`
--
ALTER TABLE `venta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `comentarios`
--
ALTER TABLE `comentarios`
  ADD CONSTRAINT `comentarios_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id`),
  ADD CONSTRAINT `comentarios_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id`);

--
-- Filtros para la tabla `detalles_pedido`
--
ALTER TABLE `detalles_pedido`
  ADD CONSTRAINT `detalles_pedido_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id`),
  ADD CONSTRAINT `detalles_pedido_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id`);

--
-- Filtros para la tabla `detalles_venta`
--
ALTER TABLE `detalles_venta`
  ADD CONSTRAINT `detalles_venta_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `venta` (`id`),
  ADD CONSTRAINT `detalles_venta_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id`);

--
-- Filtros para la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD CONSTRAINT `empleado_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`);

--
-- Filtros para la tabla `entregas_a_domicilio`
--
ALTER TABLE `entregas_a_domicilio`
  ADD CONSTRAINT `entregas_a_domicilio_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id`),
  ADD CONSTRAINT `entregas_a_domicilio_ibfk_2` FOREIGN KEY (`id_repartidor`) REFERENCES `repartidor` (`id`);

--
-- Filtros para la tabla `informacion_nutricional`
--
ALTER TABLE `informacion_nutricional`
  ADD CONSTRAINT `informacion_nutricional_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id`);

--
-- Filtros para la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD CONSTRAINT `inventario_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id`);

--
-- Filtros para la tabla `notificacion_promocion`
--
ALTER TABLE `notificacion_promocion`
  ADD CONSTRAINT `notificacion_promocion_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id`),
  ADD CONSTRAINT `notificacion_promocion_ibfk_2` FOREIGN KEY (`id_promocion`) REFERENCES `promocion` (`id`);

--
-- Filtros para la tabla `pedido`
--
ALTER TABLE `pedido`
  ADD CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id`);

--
-- Filtros para la tabla `reserva`
--
ALTER TABLE `reserva`
  ADD CONSTRAINT `reserva_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id`),
  ADD CONSTRAINT `reserva_ibfk_2` FOREIGN KEY (`id_mesa`) REFERENCES `mesa` (`id`);

--
-- Filtros para la tabla `sesion_cliente`
--
ALTER TABLE `sesion_cliente`
  ADD CONSTRAINT `sesion_cliente_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id`);

--
-- Filtros para la tabla `venta`
--
ALTER TABLE `venta`
  ADD CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`),
  ADD CONSTRAINT `venta_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
