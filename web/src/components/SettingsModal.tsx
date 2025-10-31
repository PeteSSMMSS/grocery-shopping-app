import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import api, { Product, Category } from '../lib/api'
import { useSupermarkets } from '../hooks/useSupermarkets'
import ConfirmModal from './ConfirmModal'
import Toast from './Toast'

interface SettingsModalProps {
  onClose: () => void
  products: Product[]
  categories: Category[]
  onRefresh: () => void
}

export default function SettingsModal({ onClose, products, categories, onRefresh }: SettingsModalProps) {
  const [tab, setTab] = useState<'products' | 'categories'>('products')
  
  // Editing state
  const [editingProductId, setEditingProductId] = useState<number | null>(null)
  
  // Confirmation & Toast
  const [deleteConfirm, setDeleteConfirm] = useState<{ type: 'product' | 'category'; id: number; name: string } | null>(null)
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null)
  
  // Product form
  const [productForm, setProductForm] = useState({
    name: '',
    category_id: null as number | null,
    supermarket_id: 1 as number, // Default: Netto
    price_type: 'per_package' as 'per_package' | 'per_kg' | 'per_100g' | 'per_liter',
    package_size: '',
    package_unit: 'g' as string,
    price_cents: '',
  })

  // Fetch supermarkets
  const { data: supermarkets = [] } = useSupermarkets()

  // Category form
  const [categoryForm, setCategoryForm] = useState({ name: '' })

  // Mutations
  const createProductMutation = useMutation({
    mutationFn: (data: Parameters<typeof api.products.create>[0]) =>
      api.products.create(data),
    onSuccess: () => {
      onRefresh()
      setProductForm({ name: '', category_id: null, supermarket_id: 1, price_type: 'per_package', package_size: '', package_unit: 'g', price_cents: '' })
      setToast({ message: '✅ Produkt erfolgreich erstellt!', type: 'success' })
    },
    onError: () => {
      setToast({ message: '❌ Fehler beim Erstellen des Produkts', type: 'error' })
    },
  })

  const updateProductMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => api.products.update(id, data),
    onSuccess: () => {
      onRefresh()
      setEditingProductId(null)
      setProductForm({ name: '', category_id: null, supermarket_id: 1, price_type: 'per_package', package_size: '', package_unit: 'g', price_cents: '' })
      setToast({ message: '✅ Produkt erfolgreich aktualisiert!', type: 'success' })
    },
    onError: () => {
      setToast({ message: '❌ Fehler beim Aktualisieren des Produkts', type: 'error' })
    },
  })

  const deleteProductMutation = useMutation({
    mutationFn: (id: number) => api.products.delete(id),
    onSuccess: () => {
      onRefresh()
      setDeleteConfirm(null)
      setToast({ message: '✅ Produkt erfolgreich gelöscht!', type: 'success' })
    },
    onError: () => {
      setDeleteConfirm(null)
      setToast({ message: '❌ Fehler beim Löschen des Produkts', type: 'error' })
    },
  })

  const createCategoryMutation = useMutation({
    mutationFn: (name: string) => api.categories.create(name),
    onSuccess: () => {
      onRefresh()
      setCategoryForm({ name: '' })
      setToast({ message: '✅ Kategorie erfolgreich erstellt!', type: 'success' })
    },
    onError: () => {
      setToast({ message: '❌ Fehler beim Erstellen der Kategorie', type: 'error' })
    },
  })

  const deleteCategoryMutation = useMutation({
    mutationFn: (id: number) => api.categories.delete(id),
    onSuccess: () => {
      onRefresh()
      setDeleteConfirm(null)
      setToast({ message: '✅ Kategorie erfolgreich gelöscht!', type: 'success' })
    },
    onError: () => {
      setDeleteConfirm(null)
      setToast({ message: '❌ Fehler beim Löschen der Kategorie', type: 'error' })
    },
  })

  const handleCreateProduct = (e: React.FormEvent) => {
    e.preventDefault()
    if (!productForm.name) return

    if (editingProductId) {
      // Update existing product
      updateProductMutation.mutate({
        id: editingProductId,
        data: {
          name: productForm.name,
          category_id: productForm.category_id || undefined,
          supermarket_id: productForm.supermarket_id,
          price_type: productForm.price_type,
          package_size: productForm.package_size ? parseFloat(productForm.package_size) : undefined,
          package_unit: productForm.package_unit || undefined,
          price_cents: productForm.price_cents ? parseInt(productForm.price_cents) : undefined,
        }
      })
    } else {
      // Create new product
      createProductMutation.mutate({
        name: productForm.name,
        category_id: productForm.category_id || undefined,
        supermarket_id: productForm.supermarket_id,
        price_type: productForm.price_type,
        package_size: productForm.package_size ? parseFloat(productForm.package_size) : undefined,
        package_unit: productForm.package_unit || undefined,
        price_cents: productForm.price_cents ? parseInt(productForm.price_cents) : undefined,
      })
    }
  }

  const loadProductForEdit = (product: any) => {
    setEditingProductId(product.id)
    setProductForm({
      name: product.name,
      category_id: product.category_id,
      supermarket_id: product.supermarket_id || 1,
      price_type: product.price_type,
      package_size: product.package_size?.toString() || '',
      package_unit: product.package_unit || 'g',
      price_cents: product.current_price?.toString() || '',
    })
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const resetProductForm = () => {
    setEditingProductId(null)
    setProductForm({ name: '', category_id: null, supermarket_id: 1, price_type: 'per_package', package_size: '', package_unit: 'g', price_cents: '' })
  }

  const handleCreateCategory = (e: React.FormEvent) => {
    e.preventDefault()
    if (!categoryForm.name) return
    createCategoryMutation.mutate(categoryForm.name)
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 p-4">
      <div className="bg-[#282828] rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col border border-neutral-800">
        {/* Header */}
        <div className="p-6 border-b border-neutral-800 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-neutral-100">⚙️ Einstellungen</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-neutral-700 rounded-lg text-neutral-300 transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-neutral-800">
          <button
            onClick={() => setTab('products')}
            className={`flex-1 px-4 py-3 font-medium transition-colors ${
              tab === 'products'
                ? 'border-b-2 border-red-600 text-red-500'
                : 'text-neutral-400 hover:text-neutral-200'
            }`}
          >
            Produkte
          </button>
          <button
            onClick={() => setTab('categories')}
            className={`flex-1 px-4 py-3 font-medium transition-colors ${
              tab === 'categories'
                ? 'border-b-2 border-red-600 text-red-500'
                : 'text-neutral-400 hover:text-neutral-200'
            }`}
          >
            Kategorien
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-6 bg-[#1f1f1f]">
          {tab === 'products' && (
            <div className="space-y-6">
              {/* Create/Edit Product Form */}
              <div className="bg-[#282828] p-4 rounded-lg border border-neutral-800">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-semibold text-neutral-100">
                    {editingProductId ? '✏️ Produkt bearbeiten' : '➕ Neues Produkt'}
                  </h3>
                  {editingProductId && (
                    <button
                      type="button"
                      onClick={resetProductForm}
                      className="text-sm px-3 py-1 bg-neutral-700 hover:bg-neutral-600 text-neutral-200 rounded transition"
                    >
                      Abbrechen
                    </button>
                  )}
                </div>
                <form onSubmit={handleCreateProduct} className="space-y-3">
                  <input
                    type="text"
                    placeholder="Produktname"
                    value={productForm.name}
                    onChange={(e) => setProductForm({ ...productForm, name: e.target.value })}
                    className="w-full px-3 py-2 bg-neutral-800 border border-neutral-700 text-neutral-100 placeholder-neutral-500 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                    required
                  />
                  <select
                    value={productForm.category_id || ''}
                    onChange={(e) =>
                      setProductForm({
                        ...productForm,
                        category_id: e.target.value ? Number(e.target.value) : null,
                      })
                    }
                    className="w-full px-3 py-2 bg-neutral-800 border border-neutral-700 text-neutral-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                  >
                    <option value="">Keine Kategorie</option>
                    {categories.map((cat) => (
                      <option key={cat.id} value={cat.id}>
                        {cat.name}
                      </option>
                    ))}
                  </select>
                  
                  {/* Supermarket Selection */}
                  <select
                    value={productForm.supermarket_id}
                    onChange={(e) =>
                      setProductForm({
                        ...productForm,
                        supermarket_id: Number(e.target.value),
                      })
                    }
                    className="w-full px-3 py-2 bg-neutral-800 border border-neutral-700 text-neutral-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                    required
                  >
                    {supermarkets.map((market) => (
                      <option key={market.id} value={market.id}>
                        🏪 {market.name}
                      </option>
                    ))}
                  </select>
                  
                  {/* Price Type Selection */}
                  <select
                    value={productForm.price_type}
                    onChange={(e) => setProductForm({ ...productForm, price_type: e.target.value as any })}
                    className="w-full px-3 py-2 bg-neutral-800 border border-neutral-700 text-neutral-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                  >
                    <option value="per_package">Pro Packung (Standard)</option>
                    <option value="per_kg">Pro Kilogramm (lose Ware)</option>
                    <option value="per_100g">Pro 100g</option>
                    <option value="per_liter">Pro Liter</option>
                  </select>

                  {/* Package Size and Unit - Only for per_package */}
                  {productForm.price_type === 'per_package' && (
                    <div className="flex gap-2">
                      <input
                        type="number"
                        placeholder="Größe (z.B. 500, 10, 1.5)"
                        value={productForm.package_size}
                        onChange={(e) => setProductForm({ ...productForm, package_size: e.target.value })}
                        className="flex-1 px-3 py-2 bg-neutral-800 border border-neutral-700 text-neutral-100 placeholder-neutral-500 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-500"
                        min="0.01"
                        step="0.01"
                      />
                      <select
                        value={productForm.package_unit}
                        onChange={(e) => setProductForm({ ...productForm, package_unit: e.target.value })}
                        className="w-32 px-3 py-2 bg-neutral-800 border border-neutral-700 text-neutral-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                      >
                        <option value="g">Gramm</option>
                        <option value="kg">Kilogramm</option>
                        <option value="stück">Stück</option>
                        <option value="l">Liter</option>
                        <option value="ml">Milliliter</option>
                      </select>
                    </div>
                  )}
                  
                  <input
                    type="number"
                    placeholder="Preis in Cent (z.B. 299 für 2,99€)"
                    value={productForm.price_cents}
                    onChange={(e) => setProductForm({ ...productForm, price_cents: e.target.value })}
                    className="w-full px-3 py-2 bg-neutral-800 border border-neutral-700 text-neutral-100 placeholder-neutral-500 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                  />
                  <button
                    type="submit"
                    disabled={createProductMutation.isPending || updateProductMutation.isPending}
                    className="w-full px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 font-medium transition-colors"
                  >
                    {editingProductId 
                      ? (updateProductMutation.isPending ? 'Aktualisiere...' : '💾 Produkt aktualisieren')
                      : (createProductMutation.isPending ? 'Erstelle...' : '➕ Produkt erstellen')
                    }
                  </button>
                </form>
              </div>

              {/* Products List */}
              <div>
                <h3 className="font-semibold mb-3 text-neutral-100">Alle Produkte ({products.length})</h3>
                <div className="space-y-2 max-h-96 overflow-auto">
                  {products.map((product) => (
                    <div
                      key={product.id}
                      className="flex items-center justify-between p-3 bg-[#282828] border border-neutral-800 rounded-lg hover:bg-[#2a2a2a] transition-colors"
                    >
                      <div className="flex-1">
                        <h4 className="font-medium text-neutral-100">{product.name}</h4>
                        <p className="text-sm text-neutral-400">
                          {product.current_price
                            ? `${(product.current_price / 100).toFixed(2)} €`
                            : 'Kein Preis'}
                        </p>
                      </div>
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => loadProductForEdit(product)}
                          className="px-3 py-1 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors"
                        >
                          ✏️ Bearbeiten
                        </button>
                        <button
                          onClick={() => setDeleteConfirm({ type: 'product', id: product.id, name: product.name })}
                          className="px-3 py-1 text-sm bg-red-600 hover:bg-red-700 text-white rounded transition-colors"
                        >
                          🗑️ Löschen
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {tab === 'categories' && (
            <div className="space-y-6">
              {/* Create Category Form */}
              <div className="bg-[#282828] p-4 rounded-lg border border-neutral-800">
                <h3 className="font-semibold mb-3 text-neutral-100">Neue Kategorie</h3>
                <form onSubmit={handleCreateCategory} className="space-y-3">
                  <input
                    type="text"
                    placeholder="Kategoriename"
                    value={categoryForm.name}
                    onChange={(e) => setCategoryForm({ name: e.target.value })}
                    className="w-full px-3 py-2 bg-neutral-800 border border-neutral-700 text-neutral-100 placeholder-neutral-500 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                    required
                  />
                  <button
                    type="submit"
                    disabled={createCategoryMutation.isPending}
                    className="w-full px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 font-medium transition-colors"
                  >
                    {createCategoryMutation.isPending ? 'Erstelle...' : 'Kategorie erstellen'}
                  </button>
                </form>
              </div>

              {/* Categories List */}
              <div>
                <h3 className="font-semibold mb-3 text-neutral-100">Alle Kategorien ({categories.length})</h3>
                <div className="space-y-2">
                  {categories.map((category) => (
                    <div
                      key={category.id}
                      className="flex items-center justify-between p-3 bg-[#282828] border border-neutral-800 rounded-lg"
                    >
                      <span className="font-medium text-neutral-100">{category.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <ConfirmModal
          title={deleteConfirm.type === 'product' ? 'Produkt löschen?' : 'Kategorie löschen?'}
          message={`Möchtest du "${deleteConfirm.name}" wirklich löschen? Diese Aktion kann nicht rückgängig gemacht werden.`}
          confirmText="Löschen"
          cancelText="Abbrechen"
          type="danger"
          onConfirm={() => {
            if (deleteConfirm.type === 'product') {
              deleteProductMutation.mutate(deleteConfirm.id)
            } else {
              deleteCategoryMutation.mutate(deleteConfirm.id)
            }
          }}
          onCancel={() => setDeleteConfirm(null)}
        />
      )}

      {/* Toast Notification */}
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  )
}
