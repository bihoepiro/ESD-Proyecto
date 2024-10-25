# **Informe de Seguridad y Privacidad en el Sistema de Ventas**
Alumna: Bihonda Epiquien Rodas

Curso: Ética y Seguridad de los Datos
## **1. Introducción**
Este informe documenta las medidas de seguridad implementadas en el sistema de ventas distribuido, así como estrategias de protección de datos. Además, se detallan las medidas futuras recomendadas para garantizar un sistema robusto, cumpliendo con los estándares internacionales de seguridad y privacidad.

## **2. Valor de los Datos en el Caso de Negocio**
En este sistema de ventas, los datos generan valor al permitir la **toma de decisiones basada en hechos**, como la gestión eficiente de inventarios y el análisis de ventas. Para medir este valor objetivamente, se implementarán **KPIs (Indicadores Clave de Desempeño)** como:

- **Ventas semanales por sede**: Indicador que permite analizar el rendimiento de cada tienda.
- **Tasa de crecimiento mensual de ventas**: Mide el crecimiento en ventas mes a mes.
- **Satisfacción del cliente**: Medida indirecta basada en el rendimiento de los vendedores y la disponibilidad de productos.

## **3. Protección de Datos según Normativas Locales e Internacionales**

### **3.1 Ley Peruana de Protección de Datos Personales**
La **Ley N° 29733 (Ley de Protección de Datos Personales del Perú)** establece que los datos personales deben ser tratados de forma adecuada, asegurando la privacidad y los derechos de los usuarios. En el proyecto, los datos sensibles, como nombres de vendedores y ventas históricas, están protegidos mediante políticas de acceso controlado y encriptación, lo que asegura el cumplimiento de la ley.

### **3.2 Cumplimiento de Estándares Internacionales**
En el sistema, las prácticas se alinean con estándares como el **GDPR** (Reglamento General de Protección de Datos), que exige el consentimiento explícito de los usuarios y el derecho a acceder y eliminar sus datos personales.

## **4. Medidas de Protección de Datos en Reposo y Transporte**

### **4.1 Encriptación**
Los datos sensibles del sistema están encriptados usando **bcrypt** para contraseñas, y en futuras fases, se aplicará **AES (Advanced Encryption Standard)** para encriptar los datos en reposo (datos almacenados) y en tránsito (datos que viajan entre cliente y servidor). Esto asegura que la confidencialidad de los datos sea mantenida incluso si se produce un acceso no autorizado a la base de datos.

### **4.2 Hashing**
Además de la encriptación, las contraseñas se almacenan como hashes criptográficos utilizando **bcrypt**, lo que asegura que incluso si una base de datos es comprometida, las contraseñas no pueden ser revertidas a su formato original.

### **4.3 Gestión de Accesos**
La gestión de accesos es clave en este sistema. Solo los **vendedores** pueden agregar ventas, mientras que los **supervisores** tienen permisos adicionales para revisar y modificar datos de su tienda. Los **administradores** tienen acceso completo a todos los datos. Esta separación de roles sigue las mejores prácticas de **privilegio mínimo**, donde cada usuario solo tiene acceso a lo necesario para realizar sus funciones.

### **4.4 Registros de Auditoría (Logs)** 
Se implementarán **registros de auditoría** para monitorear todas las actividades críticas del sistema, como accesos, modificaciones, y eliminaciones de datos. Estos registros permitirán detectar y responder rápidamente a actividades sospechosas, garantizando la integridad del sistema.

## **5. Estrategias de Uso Seguro de los Datos**

### **5.1 Políticas y Procedimientos**
Las políticas de uso seguro de datos están basadas en el principio de **privilegio mínimo**, lo que asegura que cada usuario solo tiene acceso a la información necesaria para realizar su trabajo. Además, se establecerán **procedimientos formales** para la recolección, almacenamiento y eliminación de datos sensibles, asegurando que todo proceso esté documentado y alineado con los estándares internacionales.

### **5.2 Concientización y Formación del Equipo**
En la próxima fase, se implementará un programa de **concientización de seguridad** para todo el personal que tenga acceso al sistema. Este programa incluirá formación sobre **mejores prácticas de seguridad**, tales como la creación de contraseñas seguras y la identificación de intentos de phishing. La educación del equipo es esencial para mantener la seguridad, dado que muchas brechas de seguridad provienen de errores humanos.

## **6. Plan de Respuesta ante Incidentes de Seguridad**

### **6.1 Plan Básico de Respuesta ante Fuga o Pérdida de Datos**
En caso de una brecha de seguridad, el sistema cuenta con un **plan de respuesta ante incidentes** que incluye:

1. **Detección rápida del incidente**: Utilizando los registros de auditoría y monitoreo en tiempo real.
2. **Aislamiento del sistema**: En caso de detección de una fuga, se desconectarán los servidores comprometidos para evitar mayores filtraciones.
3. **Recuperación y respaldo de datos**: Se implementarán **backups** periódicos y procedimientos de **recuperación ante desastres**, asegurando que los datos puedan ser restaurados rápidamente en caso de un ataque.

### **6.2 Notificación de Incidentes**
En cumplimiento con las leyes de protección de datos (como el GDPR), cualquier fuga significativa de datos personales deberá ser reportada a las autoridades competentes y a los usuarios afectados en un plazo de 72 horas.

## **7. Privacidad de los Datos**

### **7.1 Recolección de Datos**
La recolección de datos está limitada a la información necesaria para las operaciones del sistema de ventas. Solo se recopilan datos esenciales de los usuarios y clientes, como nombres y registros de ventas, respetando los principios de minimización de datos del **GDPR**.

### **7.2 Gestión del Consentimiento**
Se implementará un sistema de gestión del consentimiento que permitirá a los usuarios otorgar su consentimiento explícito antes de que sus datos sean recolectados o procesados. Este sistema también permitirá que los usuarios puedan retirar su consentimiento y solicitar la eliminación de sus datos cuando lo deseen, cumpliendo con los requisitos del GDPR y la **Ley Peruana de Protección de Datos**.

### **7.3 Anonimización de Datos**
En caso de que los datos sean utilizados para fines de análisis o reportes, se aplicarán técnicas de **anonimización** para que no sea posible identificar a los individuos. Esto asegura que los datos personales no se expongan en procesos secundarios de análisis o en investigaciones de mercado.

## **8. Recomendaciones de Protección de Datos Futura**

### **8.1 Segmentación de la Red**
Para evitar que una brecha en una parte del sistema comprometa a todo el entorno, se implementará la **segmentación de la red**, asegurando que cada tienda opere en una red separada y que los datos críticos no puedan ser accedidos desde redes no seguras.

### **8.2 Doble Factor de Autenticación**
Como se mencionó, la implementación de un sistema de **doble autenticación** es una medida clave que mejorará significativamente la seguridad, especialmente para los administradores y supervisores.

### **8.3 Cifrado Extremo a Extremo**
Se recomienda implementar **cifrado extremo a extremo** en toda la comunicación entre los clientes y el servidor, asegurando que todos los datos en tránsito estén protegidos contra interceptaciones.

## **9. Conclusión**
El sistema de ventas ha implementado medidas clave en esta primera fase, incluyendo control de acceso basado en roles y encriptación de contraseñas, lo que garantiza la protección de los datos más sensibles. En las fases siguientes, se ampliará la seguridad mediante la implementación de encriptación de datos sensibles, doble autenticación, auditorías y backups. Estas medidas asegurarán el cumplimiento con normativas locales e internacionales, protegiendo así la confidencialidad, integridad y disponibilidad de los datos.
