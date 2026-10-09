/*
    Esquema de la tienda ficticia para SQL Server.
    Las tablas se cargan desde:
        datos/clientes.csv
        datos/productos.csv
        datos/ventas.csv
        datos/detalle_ventas.csv

    El ingreso no se guarda en Ventas. Se calcula en las consultas
    con cantidad x precio_unitario, igual que en analisis_ventas.py.
*/

CREATE TABLE Clientes (
    id_cliente INT NOT NULL PRIMARY KEY,
    nombre NVARCHAR(120) NOT NULL,
    ciudad NVARCHAR(80) NOT NULL,
    fecha_registro DATE NOT NULL
);

CREATE TABLE Productos (
    id_producto INT NOT NULL PRIMARY KEY,
    producto NVARCHAR(120) NOT NULL,
    categoria NVARCHAR(80) NOT NULL,
    precio INT NOT NULL,
    costo INT NOT NULL,
    CONSTRAINT CK_Productos_Precio CHECK (precio > 0 AND costo >= 0 AND costo < precio)
);

CREATE TABLE Ventas (
    id_venta INT NOT NULL PRIMARY KEY,
    id_cliente INT NOT NULL,
    fecha_venta DATE NOT NULL,
    CONSTRAINT FK_Ventas_Clientes
        FOREIGN KEY (id_cliente) REFERENCES Clientes (id_cliente)
);

CREATE TABLE DetalleVentas (
    id_detalle INT NOT NULL PRIMARY KEY,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario INT NOT NULL,
    CONSTRAINT FK_Detalle_Ventas
        FOREIGN KEY (id_venta) REFERENCES Ventas (id_venta),
    CONSTRAINT FK_Detalle_Productos
        FOREIGN KEY (id_producto) REFERENCES Productos (id_producto),
    CONSTRAINT CK_Detalle_Cantidad CHECK (cantidad > 0 AND precio_unitario > 0)
);

CREATE INDEX IX_Ventas_Fecha ON Ventas (fecha_venta);
CREATE INDEX IX_Detalle_Venta ON DetalleVentas (id_venta);
CREATE INDEX IX_Detalle_Producto ON DetalleVentas (id_producto);

/*
    Carga recomendada: asistente de importación de SSMS, en este orden:
    Clientes, Productos, Ventas, DetalleVentas.
    Si se usa BULK INSERT, el archivo no debe quedar abierto y la ruta
    tiene que ser la del servidor. Ejemplo:

    BULK INSERT dbo.Clientes
    FROM 'C:\datos\clientes.csv'
    WITH (
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001'
    );
*/
