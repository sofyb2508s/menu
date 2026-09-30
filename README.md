# menu
<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UTB Jídelníček - Bez mléka</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background-color: #f4f6f9;
            margin: 0;
            padding: 20px;
            color: #2c3e50;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            margin-bottom: 5px;
        }
        .subtitle {
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 20px;
        }
        .legend {
            display: flex;
            justify-content: space-around;
            background: #ffffff;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-weight: bold;
            font-size: 0.9em;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .legend-item { display: flex; align-items: center; gap: 6px; }
        .dot { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }
        .dot.green { background: #2ecc71; }
        .dot.yellow { background: #f1c40f; }
        .dot.red { background: #e74c3c; }

        .date-header {
            font-size: 1.2em;
            font-weight: bold;
            margin: 20px 0 10px 0;
            padding-bottom: 5px;
            border-bottom: 2px solid #bdc3c7;
        }
        .card {
            background: #ffffff;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 6px solid #ccc;
            box-shadow: 0 2px 4px rgba(0,0,0,0.03);
        }
        .card.green { border-left-color: #2ecc71; background-color: #f0fff4; }
        .card.yellow { border-left-color: #f1c40f; background-color: #fffdf0; }
        .card.red { border-left-color: #e74c3c; background-color: #fff5f5; }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 1.05em;
            font-weight: bold;
        }
        .badge {
            padding: 4px 8px;
            border-radius: 4px;
            color: #fff;
            font-size: 0.8em;
            text-transform: uppercase;
        }
        .badge.green { background: #2ecc71; }
        .badge.yellow { background: #f1c40f; color: #000; }
        .badge.red { background: #e74c3c; }

        .allergens {
            font-size: 0.85em;
            color: #7f8c8d;
            margin-top: 8px;
        }
        .loading {
            text-align: center;
            font-size: 1.1em;
            padding: 40px;
            color: #7f8c8d;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>Jídelníček UTB</h1>
    <p class="subtitle">Filtr pro alergii na mléko a laktozu (Alergen č. 7)</p>

    <div class="legend">
        <div class="legend-item"><span class="dot green"></span> Bezpečné (Bez mléka)</div>
        <div class="legend-item"><span class="dot yellow"></span> Pozor / Možný výskyt</div>
        <div class="legend-item"><span class="dot red"></span> Obsahuje mléko (7)</div>
    </div>

    <div id="menu-container" class="loading">Načítání aktuálního jídelníčku...</div>
</div>

<script>
    async function fetchMenu() {
        const container = document.getElementById('menu-container');

        try {
            // Читаємо локальний файл menu.json, який автоматично оновлює GitHub
            const response = await fetch('menu.json?cache=' + new Date().getTime());
            if (!response.ok) throw new Error('Menu file not found');
            
            const data = await response.json();
            container.innerHTML = '';

            if (!data || data.length === 0) {
                container.innerHTML = '<p style="text-align:center;">Pro dnešní den není k dispozici žádný jídelníček.</p>';
                return;
            }

            data.forEach(day => {
                if (!day.groups || day.groups.length === 0) return;

                const dateTitle = document.createElement('div');
                dateTitle.className = 'date-header';
                dateTitle.innerText = `Datum: ${new Date(day.date).toLocaleDateString('cs-CZ')}`;
                container.appendChild(dateTitle);

                day.groups.forEach(group => {
                    group.rows.forEach(dish => {
                        const allergens = dish.allergens || '';
                        
                        let status = 'green';
                        let badgeText = 'Bezpečné';

                        const hasMilkAllergen = allergens.split(',').map(a => a.trim()).includes('7');
                        const hasMilkText = /mléko|smetan|sýr|máslo|tvaroh/i.test(dish.itemName + ' ' + allergens);

                        if (hasMilkAllergen || hasMilkText) {
                            status = 'red';
                            badgeText = 'Obsahuje mléko';
                        } else if (/stopové|možná/i.test(allergens)) {
                            status = 'yellow';
                            badgeText = 'Pozor';
                        }

                        const card = document.createElement('div');
                        card.className = `card ${status}`;
                        card.innerHTML = `
                            <div class="card-header">
                                <span>${dish.itemName}</span>
                                <span class="badge ${status}">${badgeText}</span>
                            </div>
                            <div class="allergens">
                                <strong>Alergeny:</strong> ${allergens || 'Neuvedeny'} | <strong>Cena:</strong> ${dish.price || '-'} Kč
                            </div>
                        `;
                        container.appendChild(card);
                    });
                });
            });

        } catch (error) {
            container.innerHTML = '<p style="text-align:center; color:red;">Jídelníček se právě aktualizuje. Zkuste to prosím za minutu.</p>';
        }
    }

    fetchMenu();
</script>
</body>
</html>
