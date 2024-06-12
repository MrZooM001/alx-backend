const express = require('express');
import { createClient } from 'redis';

const listProducts = [
  { Id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { Id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { Id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { Id: 4, name: 'Suitcase 1050', price: 550, stock: 5 },
];

const app = express();

const redisClient = createClient({ legacyMode: true });
redisClient.on('connect', () => {
  console.log('Redis client connected to the server');
});

redisClient.on('error', (err) => {
  console.log('Redis client not connected to the server:', err);
});

const getItemById = (id) => {
  return listProducts.find(product => product.Id === id);
};

const reserveStockById = (itemId, stock) => {
  redisClient.set(`item.${itemId}`, stock);
};

const getCurrentReservedStockById = (itemId) => {
  return new Promise((resolve, reject) => {
    redisClient.get(`item.${itemId}`, (error, result) => {
      if (error) {
        reject(error);
      } else {
        resolve(result);
      }
    });
  });
};

app.get('/list_products', (req, res) => {
  res.json(listProducts.map(product => ({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock
  })));
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);
  if (!product) {
    return res.json({ "status": "Product not found" });
  }

  const reservedStock = await getCurrentReservedStockById(itemId);
  const currentStock = product.stock - (reservedStock ? parseInt(reservedStock) : 0);
  res.json({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
    currentQuantity: currentStock
  });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);
  if (!product) {
    return res.json({ "status": "Product not found" });
  }

  const reservedStock = await getCurrentReservedStockById(itemId);
  const currentStock = product.stock - (reservedStock ? parseInt(reservedStock) : 0);
  if (currentStock <= 0) {
    return res.json({ "status": 'Not enough stock available', "itemId": itemId });
  }

  reserveStockById(itemId, (reservedStock ? parseInt(reservedStock) + 1 : 1));
  res.json({ "status": "Reservation confirmed", "itemId": itemId });
});

app.listen(1245, () => {
  console.log('Express server is listening on port 1245...');
});
