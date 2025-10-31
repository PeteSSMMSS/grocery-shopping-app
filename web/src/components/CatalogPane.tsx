import { useState, type FormEvent } from 'react'
import type { Product, Category } from '../lib/api'
import { api } from '../lib/api'

interface CatalogPaneProps {
  products: Product[]
  categories: Category[]
  onAddToList: (productId: number) => void
  supermarketId: number
  onProductCreated?: (product: Product) => void
}

export default function CatalogPane({ products, categories, onAddToList, supermarketId, onProductCreated }: CatalogPaneProps) {
  const [search, setSearch] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<number | null>(null)
  const [mode, setMode] = useState<'browse' | 'create'>('browse')
  const [creating, setCreating] = useState(false)
  // Create form state
  const [name, setName] = useState('')
  const [categoryId, setCategoryId] = useState<number | ''>('')
  const [priceCents, setPriceCents] = useState<string>('')
  const [priceType, setPriceType] = useState<'per_package' | 'per_kg' | 'per_100g' | 'per_liter'>('per_package')
  const [packageSize, setPackageSize] = useState<string>('')
  const [packageUnit, setPackageUnit] = useState<string>('')

  const resetForm = () => {
    setName('')
    setCategoryId('')
    setPriceCents('')
    setPriceType('per_package')
    setPackageSize('')
    setPackageUnit('')
  }

  const handleCreate = async (e: FormEvent) => {
    e.preventDefault()
    if (!name.trim() || !categoryId) return
    setCreating(true)
    try {
      const payload: any = {
        name: name.trim(),
        category_id: Number(categoryId),
        supermarket_id: supermarketId,
        price_type: priceType,
      }
      if (priceCents) payload.price_cents = Math.max(0, Math.round(Number(priceCents)))
      if (packageSize) payload.package_size = Number(packageSize)
      if (packageUnit) payload.package_unit = packageUnit

      const created = await api.products.create(payload)
      onProductCreated?.(created)
      // Nach Erstellung optional direkt zur Liste hinzufügen
      onAddToList(created.id)
      // zurück in den Katalog
      resetForm()
      setMode('browse')
      // Fokus zurück zur Suche
      setSearch('')
      setSelectedCategory(created.category_id ?? null)
    } catch (err) {
      console.error('Produkt-Erstellung fehlgeschlagen', err)
    } finally {
      setCreating(false)
    }
  }

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
        <div className="flex items-center justify-between">
          <h2 className="text-lg md:text-lg font-semibold text-neutral-100">Produktkatalog</h2>
          <div className="flex items-center gap-2">
            {mode === 'browse' ? (
              <button
                onClick={() => setMode('create')}
                className="px-3 py-2 bg-neutral-700 text-neutral-100 rounded-lg text-sm hover:bg-neutral-600 active:bg-neutral-600"
              >
                Neues Produkt
              </button>
            ) : (
              <button
                onClick={() => setMode('browse')}
                className="px-3 py-2 bg-neutral-700 text-neutral-100 rounded-lg text-sm hover:bg-neutral-600 active:bg-neutral-600"
              >
                Zurück
              </button>
            )}
          </div>
        </div>

        {/* Browse Mode */}
        {mode === 'browse' && (
          <>
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
          </>
        )}

        {/* Create Mode */}
        {mode === 'create' && (
          <form onSubmit={handleCreate} className="space-y-3">
            <div>
              <label className="block text-sm text-neutral-300 mb-1">Name</label>
              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                placeholder="z. B. Tomaten passiert"
                className="w-full px-4 py-3 text-base bg-neutral-800 border border-neutral-700 text-neutral-100 placeholder-neutral-500 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
              />
            </div>
            <div>
              <label className="block text-sm text-neutral-300 mb-1">Kategorie</label>
              <select
                value={categoryId}
                onChange={(e) => setCategoryId(e.target.value ? Number(e.target.value) : '')}
                required
                className="w-full px-4 py-3 bg-neutral-800 border border-neutral-700 text-neutral-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                <option value="" disabled>Kategorie wählen…</option>
                {categories.map(c => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm text-neutral-300 mb-1">Preis (Cent, optional)</label>
                <input
                  type="number"
                  min={0}
                  inputMode="numeric"
                  value={priceCents}
                  onChange={(e) => setPriceCents(e.target.value)}
                  className="w-full px-4 py-3 bg-neutral-800 border border-neutral-700 text-neutral-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                />
              </div>
              <div>
                <label className="block text-sm text-neutral-300 mb-1">Preis-Typ</label>
                <select
                  value={priceType}
                  onChange={(e) => setPriceType(e.target.value as any)}
                  className="w-full px-4 py-3 bg-neutral-800 border border-neutral-700 text-neutral-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                >
                  <option value="per_package">pro Packung</option>
                  <option value="per_kg">pro kg</option>
                  <option value="per_100g">pro 100g</option>
                  <option value="per_liter">pro Liter</option>
                </select>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-sm text-neutral-300 mb-1">Packungsgröße (optional)</label>
                <input
                  type="number"
                  min={0}
                  step="0.01"
                  inputMode="decimal"
                  value={packageSize}
                  onChange={(e) => setPackageSize(e.target.value)}
                  className="w-full px-4 py-3 bg-neutral-800 border border-neutral-700 text-neutral-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                />
              </div>
              <div>
                <label className="block text-sm text-neutral-300 mb-1">Einheit (optional)</label>
                <select
                  value={packageUnit}
                  onChange={(e) => setPackageUnit(e.target.value)}
                  className="w-full px-4 py-3 bg-neutral-800 border border-neutral-700 text-neutral-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                >
                  <option value="">—</option>
                  <option value="g">g</option>
                  <option value="kg">kg</option>
                  <option value="stück">stück</option>
                  <option value="l">l</option>
                  <option value="ml">ml</option>
                </select>
              </div>
            </div>
            <div className="flex gap-3">
              <button
                type="button"
                onClick={() => { resetForm(); setMode('browse') }}
                className="flex-1 px-4 py-3 bg-neutral-700 text-neutral-200 rounded-xl hover:bg-neutral-600 active:bg-neutral-600 font-medium"
              >
                Abbrechen
              </button>
              <button
                type="submit"
                disabled={creating}
                className="flex-1 px-4 py-3 bg-red-600 text-white rounded-xl hover:bg-red-700 active:bg-red-700 font-medium disabled:opacity-50"
              >
                {creating ? 'Speichern…' : 'Produkt hinzufügen'}
              </button>
            </div>
          </form>
        )}
      </div>

      {/* Products List - Optimized for mobile */}
      {mode === 'browse' && (
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
                <div key={categoryId} className="mb-6">
                  <h3 className="text-xs md:text-sm font-semibold text-neutral-500 uppercase mb-2 tracking-wider px-4 md:px-1">
                    {category?.name || 'Ohne Kategorie'}
                  </h3>
                  {/* Mobile: List like shopping list, Desktop: Grid */}
                  <div className="divide-y divide-neutral-700/30 md:divide-y-0 md:grid md:grid-cols-2 lg:grid-cols-3 md:gap-3">
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
                          className="w-full p-5 text-left transition active:bg-neutral-700 touch-manipulation border-b border-neutral-700/30 md:border-b-0 md:p-4 md:bg-[#282828] md:border-2 md:border-neutral-800 md:rounded-xl md:hover:border-red-500 md:hover:bg-[#2a2a2a] md:min-h-[80px] md:flex md:flex-col md:justify-between"
                        >
                          <div className="flex items-center justify-between gap-4 md:block">
                            <div className="flex-1 min-w-0 md:flex-none">
                              <h4 className="font-medium text-lg md:text-base text-neutral-100 mb-1 md:mb-2 md:line-clamp-2">
                                {product.name}
                              </h4>
                              <div className="flex items-center gap-2 text-sm text-neutral-400 md:justify-start">
                                {sizeInfo && (
                                  <>
                                    <span className="text-xs">{sizeInfo}</span>
                                    <span className="md:inline">•</span>
                                  </>
                                )}
                                <span className="font-bold text-base text-red-500 md:font-semibold md:text-neutral-100">
                                  {formatPrice(product.current_price)}
                                </span>
                              </div>
                            </div>
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
  )}
    </div>
  )
}
