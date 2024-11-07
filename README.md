# Informe de Seguridad y Privacidad en el Sistema de Ventas

**Alumna:** Bihonda Epiquien Rodas  
**Curso:** Ética y Seguridad de los Datos  

## 1. Introducción
Este informe documenta las medidas de seguridad y privacidad implementadas en el sistema de ventas, con el objetivo de proteger los datos sensibles de los usuarios y asegurar el cumplimiento de las mejores prácticas de seguridad.

## 2. Valor de los Datos en el Caso de Negocio
En este sistema de ventas, los datos generan valor al permitir la **toma de decisiones basada en hechos**, como la gestión eficiente de inventarios y el análisis de ventas. Para medir este valor objetivamente, se implementarán **KPIs (Indicadores Clave de Desempeño)** como:

- **Ventas semanales por sede**: Indicador que permite analizar el rendimiento de cada tienda.
- **Tasa de crecimiento mensual de ventas**: Mide el crecimiento en ventas mes a mes.
- **Satisfacción del cliente**: Medida indirecta basada en el rendimiento de los vendedores y la disponibilidad de productos.

## **3. Protección de Datos según Normativas Locales e Internacionales**

### **3.1 Ley Peruana de Protección de Datos Personales**
La **Ley N° 29733 (Ley de Protección de Datos Personales del Perú)** establece que los datos personales deben ser tratados de forma adecuada, asegurando la privacidad y los derechos de los usuarios. En el proyecto, los datos sensibles, como nombres de vendedores y ventas históricas, están protegidos mediante políticas de acceso controlado y encriptación, lo que asegura el cumplimiento de la ley.

### **3.2 Cumplimiento de Estándares Internacionales**
En el sistema, las prácticas se alinean con estándares como el **GDPR** (Reglamento General de Protección de Datos), que exige el consentimiento explícito de los usuarios y el derecho a acceder y eliminar sus datos personales.

## 4. Medidas de Seguridad y Protección de Datos

### 4.1 Autenticación de Dos Factores (2FA)
Para garantizar que solo usuarios autorizados accedan al sistema, se ha implementado un mecanismo de autenticación de dos factores (2FA). Este proceso asegura que, además de la contraseña, los usuarios deban verificar su identidad a través de un código temporal. Esta medida proporciona una capa de seguridad adicional, especialmente para usuarios con roles administrativos y de supervisión, reduciendo el riesgo de accesos no autorizados.

### 4.2 Encriptación y Hashing
Las contraseñas de los usuarios se protegen mediante **hashing** con el algoritmo bcrypt, una técnica que asegura que las contraseñas no puedan ser revertidas a su formato original. Esta protección es fundamental para garantizar la confidencialidad de las credenciales de acceso, incluso en caso de una brecha de seguridad en la base de datos.

### 4.3 Gestión de Accesos Basada en Roles
El sistema restringe el acceso a los datos en función del rol del usuario:
- **Vendedores:** Pueden agregar ventas para su tienda correspondiente.
- **Supervisores:** Tienen permisos adicionales para revisar los datos de ventas de su tienda.
- **Administradores:** Pueden acceder y gestionar los datos de todas las tiendas.  

Este control de acceso garantiza que cada usuario solo acceda a la información necesaria para cumplir con sus responsabilidades, minimizando el riesgo de exposición de datos.

## 5. Estrategias de Privacidad de los Datos

### 5.1 Consentimiento de Privacidad
Al acceder al sistema, los usuarios otorgan su consentimiento para el uso de sus datos personales exclusivamente para la gestión y análisis de ventas. Esta práctica asegura que los usuarios estén informados sobre el uso de su información.

### 5.2 Anonimización de Datos
Para proteger la identidad de los individuos en los análisis de ventas, los correos electrónicos y otros datos sensibles pueden ser **anonimizados**. Esto asegura que los datos personales no se expongan durante los procesos de análisis, protegiendo la privacidad de los usuarios.

### 5.3 Política de Privacidad
La política de privacidad del sistema informa a los usuarios sobre las prácticas de seguridad y sus derechos respecto a sus datos personales. Incluye información sobre los procesos de gestión del consentimiento, el acceso a sus datos y el derecho a la eliminación de la cuenta.

## **6. Plan de Respuesta ante Incidentes de Seguridad**

### **6.1 Plan Básico de Respuesta ante Fuga o Pérdida de Datos**
En caso de una brecha de seguridad, el sistema cuenta con un **plan de respuesta ante incidentes** que incluye:

1. **Detección rápida del incidente**: Utilizando los registros de auditoría y monitoreo en tiempo real.
2. **Aislamiento del sistema**: En caso de detección de una fuga, se desconectarán los servidores comprometidos para evitar mayores filtraciones.
3. **Recuperación y respaldo de datos**: Se implementarán **backups** periódicos y procedimientos de **recuperación ante desastres**, asegurando que los datos puedan ser restaurados rápidamente en caso de un ataque.

### **6.2 Notificación de Incidentes**
En cumplimiento con las leyes de protección de datos (como el GDPR), cualquier fuga significativa de datos personales deberá ser reportada a las autoridades competentes y a los usuarios afectados en un plazo de 72 horas.

## 7. Recomendaciones para Fortalecer la Seguridad

### 7.1 Encriptación de Datos Sensibles
En futuras fases, se recomienda aplicar encriptación avanzada (por ejemplo, AES) para todos los datos sensibles en reposo y en tránsito, asegurando que cualquier información comprometida se mantenga inaccesible para usuarios no autorizados.

### 7.2 Auditoría de Actividades
Implementar registros de auditoría detallados para monitorear las actividades de los usuarios en el sistema permitiría detectar comportamientos inusuales y prevenir posibles accesos indebidos a la información.

### 7.3 Concientización sobre Seguridad
Se recomienda un programa de capacitación para los usuarios con acceso al sistema, donde se refuercen prácticas de seguridad, como el uso de contraseñas fuertes y la identificación de intentos de phishing.

## 8. Conclusión
En esta fase del sistema de ventas, se han implementado medidas clave para garantizar la seguridad y privacidad de los datos, incluyendo la autenticación de dos factores y el control de acceso basado en roles. Estas prácticas fortalecen la protección de la información, asegurando un entorno seguro para la gestión de ventas y cumpliendo con las mejores prácticas de seguridad de datos.
