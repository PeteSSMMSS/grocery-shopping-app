import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from './lib/api'
import ListPane from './components/ListPane'
import CatalogPane from './components/CatalogPane'
import SettingsModal from './components/SettingsModal'
import MealsModal from './components/MealsModal'
import CalendarModal from './components/CalendarModal'
import Toast from './components/Toast'

function App() {
  const queryClient = useQueryClient()
  const [isSettingsOpen, setIsSettingsOpen] = useState(false)
  const [isMealsOpen, setIsMealsOpen] = useState(false)
  const [isCalendarOpen, setIsCalendarOpen] = useState(false)
  const [isCatalogOpen, setIsCatalogOpen] = useState(false)
  const [online, setOnline] = useState(navigator.onLine)
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null)

  window.addEventListener('online', () => setOnline(true))
  window.addEventListener('offline', () => setOnline(false))

  const { data: activeList, isLoading } = useQuery({
    queryKey: ['activeList'],
    queryFn: () => api.list.getActive(),
    refetchInterval: online ? 10000 : false,
  })

  const { data: products = [] } = useQuery({
    queryKey: ['products'],
    queryFn: () => api.products.getAll({ active: true }),
  })

  const { data: categories = [] } = useQuery({
    queryKey: ['categories'],
    queryFn: () => api.categories.getAll(),
  })

  const addItemMutation = useMutation({
    mutationFn: ({ product_id, qty }: { product_id: number; qty: number }) =>
      api.list.addItem(product_id, qty),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['activeList'] })
    },
  })

  const updateItemMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: { qty?: number; is_checked?: boolean } }) =>
      api.list.updateItem(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['activeList'] })
    },
  })

  const removeItemMutation = useMutation({
    mutationFn: (id: number) => api.list.removeItem(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['activeList'] })
    },
  })

  const checkoutMutation = useMutation({
    mutationFn: () => api.purchase.checkout(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['activeList'] })
    },
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-[#1f1f1f]">
        <div className="text-xl text-neutral-300">Lade...</div>
      </div>
    )
  }

  return (
    <div className="h-screen flex flex-col bg-[#1f1f1f]">
      <header className="bg-[#282828] shadow-lg border-b border-neutral-800">
        <div className="px-4 py-3 md:py-4 flex items-center justify-between">
          <div className="flex items-center gap-2 md:gap-3">
            <h1 className="text-xl md:text-2xl font-bold text-neutral-100">🛒 Einkaufsliste</h1>
            {!online && (
              <span className="px-2 py-1 text-xs font-medium bg-amber-600 text-amber-100 rounded">
                Offline
              </span>
            )}
          </div>
          <div className="flex items-center gap-2">
            {/* Desktop: Full buttons */}
            <div className="hidden md:flex items-center gap-2">
              <button
                onClick={() => checkoutMutation.mutate()}
                disabled={!activeList?.items.length || checkoutMutation.isPending}
                className="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium transition-colors"
              >
                {checkoutMutation.isPending ? 'Erledigt...' : '✓ Erledigt'}
              </button>
              <button
                onClick={() => setIsCalendarOpen(true)}
                className="px-4 py-2 bg-neutral-700 text-neutral-200 rounded-lg hover:bg-neutral-600 font-medium transition-colors"
              >
                📅 Kalender
              </button>
              <button
                onClick={() => setIsMealsOpen(true)}
                className="px-4 py-2 bg-neutral-700 text-neutral-200 rounded-lg hover:bg-neutral-600 font-medium transition-colors"
              >
                🍳 Mahlzeiten
              </button>
              <button
                onClick={() => setIsSettingsOpen(true)}
                className="px-4 py-2 bg-neutral-700 text-neutral-200 rounded-lg hover:bg-neutral-600 font-medium transition-colors"
              >
                ⚙️ Einstellungen
              </button>
            </div>

            {/* Mobile: Only "Erledigt" button */}
            <div className="flex md:hidden items-center gap-1">
              <button
                onClick={() => {
                  if (window.confirm('Möchtest du den Einkauf wirklich als erledigt markieren?')) {
                    checkoutMutation.mutate()
                  }
                }}
                disabled={!activeList?.items.length || checkoutMutation.isPending}
                className="px-4 py-2 bg-emerald-600 text-white rounded-lg active:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
                title="Einkauf erledigen"
              >
                {checkoutMutation.isPending ? 'Wird erledigt...' : 'Erledigt'}
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="flex-1 overflow-hidden">
        <div className="h-full flex flex-col md:flex-row">
          {/* Mobile: Only List, Catalog as Modal */}
          <div className="w-full md:w-1/2 md:border-r border-neutral-800 overflow-auto bg-[#282828]">
            <ListPane
              list={activeList}
              onUpdateItem={(id, data) => updateItemMutation.mutate({ id, data })}
              onRemoveItem={(id) => removeItemMutation.mutate(id)}
            />
          </div>

          {/* Desktop: Catalog side-by-side */}
          <div className="hidden md:block w-full md:w-1/2 overflow-auto bg-[#1f1f1f]">
            <CatalogPane
              products={products}
              categories={categories}
              onAddToList={(productId) => addItemMutation.mutate({ product_id: productId, qty: 1 })}
            />
          </div>
        </div>
      </main>

      {/* Mobile: Floating Action Button to open Catalog */}
      <button
        onClick={() => setIsCatalogOpen(true)}
        className="md:hidden fixed bottom-6 right-6 w-16 h-16 bg-red-600 hover:bg-red-700 active:bg-red-800 text-white rounded-full shadow-2xl flex items-center justify-center z-50 touch-manipulation"
        aria-label="Produktkatalog öffnen"
      >
        <span className="text-3xl leading-none">+</span>
      </button>

      {/* Mobile: Catalog Modal - Fullscreen */}
      {isCatalogOpen && (
        <div className="md:hidden fixed inset-0 bg-[#1f1f1f] z-50 flex flex-col">
          {/* Modal Header */}
          <div className="bg-[#282828] p-4 flex items-center justify-between border-b border-neutral-800">
            <h2 className="text-xl font-bold text-neutral-100">Produkte hinzufügen</h2>
            <button
              onClick={() => setIsCatalogOpen(false)}
              className="p-2 text-neutral-400 hover:text-neutral-100 active:bg-neutral-700 rounded-lg transition-colors"
            >
              ✕
            </button>
          </div>
          {/* Modal Content - Full height */}
          <div className="flex-1 overflow-auto">
            <CatalogPane
              products={products}
              categories={categories}
              onAddToList={(productId) => {
                addItemMutation.mutate({ product_id: productId, qty: 1 })
                setToast({ message: '✅ Zur Liste hinzugefügt!', type: 'success' })
              }}
            />
          </div>
        </div>
      )}

      {isMealsOpen && (
        <MealsModal
          onClose={() => setIsMealsOpen(false)}
          products={products}
          onRefresh={() => {
            queryClient.invalidateQueries({ queryKey: ['meals'] })
          }}
        />
      )}

      {isSettingsOpen && (
        <SettingsModal
          onClose={() => setIsSettingsOpen(false)}
          products={products}
          categories={categories}
          onRefresh={() => {
            queryClient.invalidateQueries({ queryKey: ['products'] })
            queryClient.invalidateQueries({ queryKey: ['categories'] })
          }}
        />
      )}

      {isCalendarOpen && (
        <CalendarModal
          onClose={() => setIsCalendarOpen(false)}
        />
      )}

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

export default App
