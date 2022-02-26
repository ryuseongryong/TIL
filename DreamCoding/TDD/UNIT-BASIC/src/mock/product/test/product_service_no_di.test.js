const ProductService = require('../product_service_no_di.js');
const ProductClient = require('../product_client.js');
jest.mock('../product_client');

describe('ProductService', () => {
  const fetchItems = jest.fn(async () => [
    { item: 'Milk', available: true },
    { item: 'Banana', available: false },
  ]);
  ProductClient.mockImplementation(() => {
    return {
      fetchItems,
    };
  });
  let productService;

  beforeEach(() => {
    productService = new ProductService();
    // jest.config.js - clearMocks: false,
    // fetchItems.mockClear()
    // ProductClient.mockClear()
  });

  it('should filter out only available items', async () => {
    const items = await productService.fetchAvailableItems();
    expect(items).toEqual([{ item: 'Milk', available: true }]);
    // jest.config.js - clearMocks: true,
    expect(items.length).toBe(1);
  });

  it('test', async () => {
    const items = await productService.fetchAvailableItems();
    expect(fetchItems).toHaveBeenCalledTimes(1);
  });
});
