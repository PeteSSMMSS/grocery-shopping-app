import type { ActiveList } from '../lib/api'

interface ListPaneProps {
  list?: ActiveList
  onUpdateItem: (id: number, data: { qty?: number; is_checked?: boolean }) => void
  onRemoveItem: (id: number) => void
}

export default function ListPane({ list, onUpdateItem, onRemoveItem }: ListPaneProps) {
  if (!list) {
    return (
      <div className="p-8 text-center text-neutral-400 bg-[#282828] h-full">
        <p>Liste wird geladen...</p>
      </div>
    )
  }

  const formatPrice = (cents: number | null) => {
    if (!cents) return '—'
    return `${(cents / 100).toFixed(2)} €`
  }

  return (
    <div className="flex flex-col h-full bg-[#282828]">
      <div className="p-4 bg-[#282828] border-b border-neutral-800">
        <h2 className="text-lg font-semibold text-neutral-100">{list.name}</h2>
        <p className="text-sm text-neutral-400">{list.items.length} Artikel</p>
      </div>

      {/* Items List */}
      <div className="flex-1 overflow-auto">
        {list.items.length === 0 ? (
          <div className="p-8 text-center text-neutral-400">
            <p>Keine Artikel auf der Liste</p>
            <p className="text-sm mt-2">Füge Produkte aus dem Katalog hinzu →</p>
          </div>
        ) : (
          <div className="divide-y divide-neutral-700/30">
            {list.items.map((item) => (
              <div
                key={item.id}
                onClick={() => onUpdateItem(item.id, { is_checked: !item.is_checked })}
                className={`p-3 md:p-4 hover:bg-neutral-700 active:bg-neutral-700 transition cursor-pointer border-l-2 ${
                  item.is_checked 
                    ? 'bg-neutral-800 opacity-70 border-l-neutral-700' 
                    : 'bg-[#282828] border-l-transparent hover:border-l-neutral-600'
                }`}
              >
                <div className="flex items-center gap-3 md:gap-3">
                  {/* Checkbox - Larger on mobile */}
                  <input
                    type="checkbox"
                    checked={item.is_checked}
                    onChange={(e) => {
                      e.stopPropagation()
                      onUpdateItem(item.id, { is_checked: e.target.checked })
                    }}
                    onClick={(e) => e.stopPropagation()}
                    className="w-6 h-6 md:w-5 md:h-5 text-red-600 bg-neutral-700 border-neutral-600 rounded focus:ring-red-500"
                  />

                  {/* Product Info */}
                  <div className="flex-1 min-w-0">
                    <h3
                      className={`font-medium text-base md:text-base ${
                        item.is_checked ? 'line-through text-neutral-500' : 'text-neutral-100'
                      }`}
                    >
                      {item.product.name}
                    </h3>
                    {item.product.current_price && (
                      <div className="text-xs text-neutral-600 mt-0.5">
                        {formatPrice(item.product.current_price)} × {item.qty}
                      </div>
                    )}
                  </div>

                  {/* Quantity Controls - Larger on mobile */}
                  <div className="flex items-center gap-1 md:gap-2" onClick={(e) => e.stopPropagation()}>
                    <button
                      onClick={() =>
                        item.qty > 1
                          ? onUpdateItem(item.id, { qty: item.qty - 1 })
                          : onRemoveItem(item.id)
                      }
                      className="w-9 h-9 md:w-8 md:h-8 flex items-center justify-center bg-neutral-700 hover:bg-neutral-600 active:bg-neutral-600 rounded text-neutral-200 font-bold transition-colors touch-manipulation"
                    >
                      −
                    </button>
                    <span className="w-9 md:w-8 text-center font-medium text-neutral-200">{item.qty}</span>
                    <button
                      onClick={() => onUpdateItem(item.id, { qty: item.qty + 1 })}
                      className="w-9 h-9 md:w-8 md:h-8 flex items-center justify-center bg-neutral-700 hover:bg-neutral-600 active:bg-neutral-600 rounded text-neutral-200 font-bold transition-colors touch-manipulation"
                    >
                      +
                    </button>
                  </div>

                  {/* Remove Button - Larger on mobile */}
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      onRemoveItem(item.id)
                    }}
                    className="p-2 md:p-2 text-red-400 hover:bg-red-900 active:bg-red-900 hover:bg-opacity-20 active:bg-opacity-30 rounded transition-colors touch-manipulation"
                    title="Entfernen"
                  >
                    🗑️
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Total Bar */}
      <div className="p-4 bg-[#282828] border-t-2 border-neutral-800">
        <div className="flex items-center justify-between">
          <span className="text-lg font-medium text-neutral-300">Gesamt:</span>
          <span className="text-2xl font-bold text-red-500">
            {formatPrice(list.total_cents)}
          </span>
        </div>
      </div>
    </div>
  )
}
