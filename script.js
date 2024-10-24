let vendedorId = null;

// Function to authenticate the user
function authenticate() {
    vendedorId = document.getElementById('vendedor_id').value;
    if (!vendedorId) {
        document.getElementById('auth_message').textContent = "Por favor ingresa un Vendedor ID.";
        return;
    }
    document.getElementById('auth_message').textContent = "Autenticación exitosa.";
}

// Function to view sales for a store
async function viewSales() {
    if (!vendedorId) {
        document.getElementById('auth_message').textContent = "Autentícate primero.";
        return;
    }

    const store = document.getElementById('store_view').value;

    try {
        const response = await fetch(`/ventas/${store}?vendedor_id=${vendedorId}`);

        if (!response.ok) {
            throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }

        const data = await response.json();
        console.log("Response data:", data);  // Debugging: Check what data is being received

        const salesList = document.getElementById('sales_list');
        salesList.innerHTML = '';  // Clear previous results

        if (data.error) {
            salesList.textContent = data.error;
            console.log("Error from server:", data.error);  // Debugging log
        } else if (data.length === 0) {
            salesList.textContent = "No se encontraron ventas para esta sede.";
            console.log("No sales data found.");  // Debugging log
        } else {
            data.forEach(sale => {
                const saleItem = document.createElement('div');
                saleItem.classList.add('sales-item');
                saleItem.textContent = `Fecha: ${sale.Date}, Ventas: ${sale.Weekly_Sales}, Sede: ${sale.Store}`;
                salesList.appendChild(saleItem);
            });
        }
    } catch (error) {
        console.error("Error fetching sales data:", error);  // Debugging: log any fetch errors
        document.getElementById('sales_list').textContent = "Hubo un error al cargar las ventas.";
    }
}


// Function to add a sale
async function addSale() {
    if (!vendedorId) {
        document.getElementById('auth_message').textContent = "Autentícate primero.";
        return;
    }

    const data = {
        vendedor_id: vendedorId,
        Store: document.getElementById('store_add').value,
        Date: document.getElementById('date').value,
        Weekly_Sales: document.getElementById('weekly_sales').value,
        Holiday_Flag: document.getElementById('holiday_flag').checked ? 1 : 0,
        Temperature: document.getElementById('temperature').value,
        Fuel_Price: document.getElementById('fuel_price').value,
        CPI: document.getElementById('cpi').value
    };

    try {
        const response = await fetch('/agregar_venta', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        const messageElement = document.getElementById('add_sale_message');

        if (response.ok) {
            messageElement.textContent = result.message;
            console.log("Sale added successfully:", result);  // Debugging log
        } else {
            messageElement.textContent = result.error;
            console.log("Error adding sale:", result.error);  // Debugging log
        }
    } catch (error) {
        console.error("Error adding sale:", error);  // Debugging: log any fetch errors
        document.getElementById('add_sale_message').textContent = "Hubo un error al agregar la venta.";
    }
}
