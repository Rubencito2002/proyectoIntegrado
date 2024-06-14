[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/zSeAaPCY)

# Proyecto Integral de Fin de Grado. (CFGS Desarrollo de Apliaciones Web)

* Se solicita lo siguiente para la realización de este proyecto:
**Se va realizar tres aplicaciones para la realizacion de este proyecto.**
## Aplicación de Almacen (almacenApp):
* **Creacción de los modelos** necesario para su alta y administracion en django admin.
**Todos los enlances de la aplicacion por defecto estan en la ruta almacen/...**     
* **CRUD de Productos** en la ruta productos/
    * **listado** de los productos que debera tener enlances para el resto de acciones, es posible buscar y filtrar por varios campos.
    * **edicion/\<int:pk>** Editar información de un producto.
    * **eliminar/\<int:pk>** Debe solicitar confirmación.
    * **nuevo** Permite introducir un nuevo producto.
    * **detalles** se realiza una vista para mostrar los detalles de un producto.
* **CRUD de Proveedor** necesario para poder crear los pedidos que tiene lugar en proveedor/
    * **listado** de los proveedores que debe tener enlances para el resto de acciones.
    * **edicion/\<int:pk>** Editar información de un proveedor.
    * **eliminar/\<int:pk>/** Debe solicitar una confirmación.
    * **nuevo** Permite introducir nuevos proveedores.
* **CRUD de Marca** necesario para poder crear los productos que tiene lugar en marca/
    * **listado** de las marcas que debe tener enlances para el resto de acciones.
    * **edicion/\<int:pk>** Editar información de una marca.
    * **eliminar/\<int:pk>/** Debe solicitar una confirmación.
    * **nuevo** Permite introducir nuevas marcas.
* **CRUD de Categoria** necesario para poder crear los productos que tiene lugar en categoria/
    * **listado** de las categorias que debe tener enlances para el resto de acciones.
    * **edicion/\<int:pk>** Editar información de una categoria.
    * **eliminar/\<int:pk>/** Debe solicitar una confirmación.
    * **nuevo** Permite introducir nuevas categorias.
* **Gestionar Pedidos**. Tiene lugar en la ruta pedidos/
    * **pedidos** se muestra un listado de productos que estaran ordenados por de menor a mayor cantidad de cada producto.
    * **solicitar** se muestra los detalles del producto, se introduce las unidades y el proveedor para poder realizar el pedido.
    * **confirmar** se realiza una confirmacion de pedido para poder actualizar los datos de ese producto con el pedido realizado anteriormente.
    * **detalles** se realiza una vista para mostrar los detalles de un pedido.
* **Informes** En la ruta de informes/
    * Listado de los pedidos por su estado, por su usuarios y por su proveedor.
    * Listado de productos por los más pedidos.
    * Listado de los usuarios más activos (Exclusivo como usuario con el rol de Empleado).
    * Listado de las ventas del comercio.
* **Control de Permisos**
    * Las secciones de admin, las creacciones del modelo, informes es sólo para usuarios tipos superuser y staff.
    * La seccion de pedidos deben estar restringidos a usuarios registrados como usuario empleados sin permisos de staff e superuser.
    * Las vistas de productos y detalles de productos tambien debe estar restringidos a usuarios registrados como usuario empleados sin permisos de staff e superuser.
## Aplicación de Tienda (tiendaApp):
**Todos los enlances de la aplicacion por defecto estan en la ruta /...**     
* **Gestion de Productos** en la ruta /
    * **listadoGeneral** listado de los productos que debera tener enlances para el resto de acciones, es posible buscar y filtrar por varios campos.
    * **listadoSupermercado/** listado de los productos exclusivo de la categoria de supermercado.        
    * **listadoModa/** listado de los productos exclusivo de la categoria de moda.
    * **listadoInformatica/** listado de los productos exclusivo de la categoria de supermercado.
* **Gestion de Compra**. Tiene lugar en la ruta comprar/
    * **procesarCompra** se realiza un procesado de todo el contenido que se rellena en el carrito de compra para poder realizar la compra de todos los productos seleccionado, ya que los datos del carrito se le esta pasando al backend a traves del fronted para que el backend no tenga tanta carga.
    * **confirmar** se realiza una confirmacion de compra donde se muestra los detalles de todos los productos que estaban en el carrito, tambien se muestra varios formularios donde se recoge los datos de la forma de envio de los productos y de la forma de pago que se va a realizar.
* **Valoracion**. Tiene lugar en la ruta valoracion/
    * **valoracion/<int:pk>** Se realiza la creaccion de la valoracion de los productos dentro de la propia pagina de detalles del producto.
    * **ediccion** donde se podra modificar los datos de esa valoracion por si se te ha pasado algo que aporta.
* **Control de Permisos**
    * La seccion de compras deben estar restringidos a usuarios registrados como usuario clientes sin permisos de staff e superuser.
    * Las vistas de productos y detalles de productos tambien debe estar restringidos a usuarios registrados como usuario clientes sin permisos de staff e superuser.
## Aplicación de Gestion de Usuarios (gestionUsuarios):
**Todos los enlances de la aplicacion por defecto estan en la ruta usuarios/...**   
* **Registro de Usuarios**. Tiene lugar en la ruta register/
    * Donde se realizará a través de un único formulario el registro de los usuarios tanto empleados como clientes.
    * Cuando se realiza el registro de los usuarios se nos mostrará una nueva página mostrando que el usuario se ha creado.
* **Página de Login**. Tiene lugar en la ruta login/
    * Donde se realizará a través de un único formulario que se le pide al usuario su nombre de usuario y contraseña para iniciar sesión
* **Página de Cierre de Sesión**. Tiene lugar en la ruta valoracion/
    * Donde se realizará el cierre de sesión del usuario y se pasará a la página principal.
* **Panel de Perfil**. Tiene lugar en la ruta perfil/
    * Donde se mostrará una página donde se muestre los datos del usuario.
    * En este panel el usuario podrá modificar datos de su perfil como cambiar la contraseña.
    * En este panel se mostrarán los pedidos que realiza los empleados como las compras que realiza los clientes, también para los clientes se le mostrará las valoraciones que realiza y también el listado de los productos favoritos de los clientes.
## Futuras Versiones:
### Aplicacion de Api.
    * Se ha generado una nueva aplicación llamada api para poder searializar nuestro modelo actual de nuestra aplicación.