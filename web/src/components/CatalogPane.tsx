import { useState } from 'react'
import type { Product, Category } from '../lib/api'

interface CatalogPaneProps {
  products: Product[]
  categories: Category[]
  onAddToList: (productId: number) => void
}

export default function CatalogPane({ products, categories, onAddToList }: CatalogPaneProps) {
  const [search, setSearch] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<number | null>(null)

  const formatPrice = (cents: number | null) => {
    if (!cents) return 'Kein Preis'
    return `${(cents / 100).toFixed(2)} €`
  }

  // Filter products
  const filteredProducts = products.filter((product) => {
    const matchesSearch = product.name.toLowerCase().includes(search.toLowerCase())
    const matchesCategory = selectedCategory === null || product.category_id === selectedCategory
    return matchesSearch && matchesCategory
  })

  // Group products by category
  const grouped = filteredProducts.reduce((acc, product) => {
    const categoryId = product.category_id || 0
    if (!acc[categoryId]) acc[categoryId] = []
    acc[categoryId].push(product)
    return acc
  }, {} as Record<number, Product[]>)

  return (
    <div className="flex flex-col h-full bg-[#1f1f1f]">
      <div className="p-3 md:p-4 bg-[#282828] border-b border-neutral-800 space-y-3">
        <h2 className="text-lg md:text-lg font-semibold text-neutral-100">Produktkatalog</h2>

        {/* Search - Larger on mobile */}
        <input
          type="text"
          placeholder="Produkt suchen..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full px-4 py-3 md:py-2 text-base bg-neutral-800 border border-neutral-700 text-neutral-100 placeholder-neutral-500 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
        />

        {/* Category Filter - Larger buttons on mobile */}
        <div className="flex gap-2 flex-wrap">
          <button
            onClick={() => setSelectedCategory(null)}
            className={`px-4 py-2 md:px-3 md:py-1 rounded-lg text-sm font-medium transition touch-manipulation ${
              selectedCategory === null
                ? 'bg-red-600 text-white'
                : 'bg-neutral-700 text-neutral-300 active:bg-neutral-600'
            }`}
          >
            Alle
          </button>
          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={`px-4 py-2 md:px-3 md:py-1 rounded-lg text-sm font-medium transition touch-manipulation ${
                selectedCategory === cat.id
                  ? 'bg-red-600 text-white'
                  : 'bg-neutral-700 text-neutral-300 active:bg-neutral-600'
              }`}
            >
              {cat.name}
            </button>
          ))}
        </div>
      </div>

      {/* Products List - Optimized for mobile */}
      <div className="flex-1 overflow-auto p-3 md:p-4">
        {filteredProducts.length === 0 ? (
          <div className="text-center text-neutral-400 py-12">
            <div className="text-5xl mb-3">🔍</div>
            <p className="text-lg">Keine Produkte gefunden</p>
          </div>
        ) : (
          <div className="space-y-6">
            {Object.entries(grouped).map(([categoryId, categoryProducts]) => {
              const category = categories.find((c) => c.id === Number(categoryId))
              return (
                <div key={categoryId}>
                  <h3 className="text-xs md:text-sm font-semibold text-neutral-500 uppercase mb-3 tracking-wider px-1">
                    {category?.name || 'Ohne Kategorie'}
                  </h3>
                  {/* Mobile: Single column list, Desktop: Grid */}
                  <div className="space-y-2 md:space-y-0 md:grid md:grid-cols-2 lg:grid-cols-3 md:gap-3">
                    {categoryProducts.map((product) => {
                      // Generate meta info based on price type
                      let sizeInfo = ''
                      if (product.price_type === 'per_kg') {
                        sizeInfo = 'pro kg'
                      } else if (product.price_type === 'per_100g') {
                        sizeInfo = 'pro 100g'
                      } else if (product.price_type === 'per_liter') {
                        sizeInfo = 'pro Liter'
                      } else if (product.price_type === 'per_package' && product.package_size) {
                        const unit = product.package_unit || 'Stück'
                        sizeInfo = `${product.package_size}${unit} Packung`
                      }
                      
                      return (
                        <button
                          key={product.id}
                          onClick={() => onAddToList(product.id)}
                          className="w-full p-4 md:p-4 bg-[#282828] border-2 border-neutral-800 rounded-xl active:border-red-500 active:bg-[#2a2a2a] transition text-left touch-manipulation min-h-[80px] flex flex-col justify-between"
                        >
                          <h4 className="font-medium text-base md:text-base text-neutral-100 mb-2 line-clamp-2">
                            {product.name}
                          </h4>
                          <div className="flex items-center justify-between gap-2 text-sm text-neutral-400">
                            {sizeInfo && (
                              <span className="text-xs">{sizeInfo}</span>
                            )}
                            <span className="font-bold text-base text-red-500 ml-auto">
                              {formatPrice(product.current_price)}
                            </span>
                          </div>
                        </button>
                      )
                    })}
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
