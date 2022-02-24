function fetchProduct(error) {
  if (error === 'error') {
    return Promise.reject('network error');
  }
  return Promise.resolve({ item: 'Milk', price: 200 });
}

module.exports = fetchProduct;
