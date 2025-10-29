import type { ActiveList } from '../lib/api'

interface ListPaneProps {
  list?: ActiveList
  onUpdateItem: (id: number, data: { qty?: number; is_checked?: boolean }) => void
  onRemoveItem: (id: number) => void
}

export default function ListPane({ list, onUpdateItem, onRemoveItem }: ListPaneProps) {
  // Format price helper
  const formatPrice = (cents: number | null) => {
    if (!cents) return '—'
    return `${(cents / 100).toFixed(2)} €`
  }

  if (!list) {
    return (
      <div className="p-8 text-center text-neutral-400 bg-[#282828] h-full">
        <p>Liste wird geladen...</p>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full bg-[#282828]">
      {/* Items List - No header, full space for shopping */}
      <div className="flex-1 overflow-auto">
        {list.items.length === 0 ? (
          <div className="p-8 text-center text-neutral-400">
            <div className="text-6xl mb-4">🛒</div>
            <p className="text-lg font-medium mb-2">Keine Artikel</p>
            <p className="text-sm">Tippe auf + um Produkte hinzuzufügen</p>
          </div>
        ) : (
          <div className="divide-y divide-neutral-700/30">
            {list.items.map((item) => (
              <button
                key={item.id}
                onClick={() => onUpdateItem(item.id, { is_checked: !item.is_checked })}
                className={`w-full p-5 md:p-4 text-left transition active:bg-neutral-700 ${
                  item.is_checked 
                    ? 'bg-neutral-800/50 opacity-60' 
                    : 'bg-[#282828] hover:bg-neutral-700/30'
                }`}
              >
                <div className="flex items-center justify-between gap-4">
                  {/* Product name with quantity */}
                  <div className="flex-1 min-w-0">
                    <h3
                      className={`font-medium text-lg md:text-base transition ${
                        item.is_checked 
                          ? 'line-through text-neutral-500' 
                          : 'text-neutral-100'
                      }`}
                    >
                      {item.qty > 1 && <span className="text-neutral-400 mr-2">{item.qty}×</span>}
                      {item.product.name}
                    </h3>
                  </div>

                  {/* Delete Button - Only visible when checked */}
                  {item.is_checked && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        onRemoveItem(item.id)
                      }}
                      className="flex-shrink-0 p-2 text-neutral-600 hover:text-red-400 active:text-red-500 transition-colors"
                      title="Entfernen"
                    >
                      🗑️
                    </button>
                  )}
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Total Bar - Always visible */}
      {list.items.length > 0 && (
        <div className="p-4 bg-[#282828] border-t-2 border-neutral-800">
          <div className="flex items-center justify-between">
            <span className="text-lg font-medium text-neutral-300">Gesamt:</span>
            <span className="text-2xl font-bold text-red-500">
              {formatPrice(list.total_cents)}
            </span>
          </div>
        </div>
      )}
    </div>
  )
}
