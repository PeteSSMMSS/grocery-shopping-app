import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api, { type Product, type MealIngredientCreate } from '../lib/api'
import Toast from './Toast'
import ConfirmModal from './ConfirmModal'

interface MealsModalProps {
  onClose: () => void
  products: Product[]
  onRefresh: () => void
}

interface IngredientInput {
  product_id: number
  quantity: number
  quantity_unit: string
}

const MEAL_TYPES = [
  { value: 'breakfast', label: 'Frühstück', emoji: '🌅' },
  { value: 'lunch', label: 'Mittagessen', emoji: '🍽️' },
  { value: 'dinner', label: 'Abendessen', emoji: '🌙' },
] as const

export default function MealsModal({ onClose, products, onRefresh }: MealsModalProps) {
  const queryClient = useQueryClient()
  const [showForm, setShowForm] = useState(false)
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null)
  const [deleteConfirm, setDeleteConfirm] = useState<{ id: number; name: string } | null>(null)
  const [editingMealId, setEditingMealId] = useState<number | null>(null)

  // Form state
  const [mealForm, setMealForm] = useState({
    name: '',
    meal_type: 'lunch' as 'breakfast' | 'lunch' | 'dinner',
    preparation: '',
  })
  const [ingredients, setIngredients] = useState<IngredientInput[]>([])

  // Fetch meals
  const { data: meals = [] } = useQuery({
    queryKey: ['meals'],
    queryFn: () => api.meals.getAll(),
  })

  // Create mutation
  const createMealMutation = useMutation({
    mutationFn: (data: { name: string; meal_type: 'breakfast' | 'lunch' | 'dinner'; preparation?: string; ingredients: MealIngredientCreate[] }) =>
      api.meals.create(data),
    onSuccess: () => {
      onRefresh()
      queryClient.invalidateQueries({ queryKey: ['meals'] })
      resetForm()
      setShowForm(false)
      setEditingMealId(null)
      setToast({ message: '✅ Mahlzeit erfolgreich erstellt!', type: 'success' })
    },
    onError: () => {
      setToast({ message: '❌ Fehler beim Erstellen der Mahlzeit', type: 'error' })
    },
  })

  // Update mutation
  const updateMealMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: { name: string; meal_type: 'breakfast' | 'lunch' | 'dinner'; preparation?: string; ingredients: MealIngredientCreate[] } }) =>
      api.meals.update(id, data),
    onSuccess: () => {
      onRefresh()
      queryClient.invalidateQueries({ queryKey: ['meals'] })
      resetForm()
      setShowForm(false)
      setEditingMealId(null)
      setToast({ message: '✅ Mahlzeit erfolgreich aktualisiert!', type: 'success' })
    },
    onError: () => {
      setToast({ message: '❌ Fehler beim Aktualisieren der Mahlzeit', type: 'error' })
    },
  })

  // Delete mutation
  const deleteMealMutation = useMutation({
    mutationFn: (id: number) => api.meals.delete(id),
    onSuccess: () => {
      onRefresh()
      queryClient.invalidateQueries({ queryKey: ['meals'] })
      setDeleteConfirm(null)
      setToast({ message: '✅ Mahlzeit erfolgreich gelöscht!', type: 'success' })
    },
    onError: () => {
      setDeleteConfirm(null)
      setToast({ message: '❌ Fehler beim Löschen der Mahlzeit', type: 'error' })
    },
  })

  const resetForm = () => {
    setEditingMealId(null)
    setMealForm({ name: '', meal_type: 'lunch', preparation: '' })
    setIngredients([])
  }

  const addIngredient = () => {
    setIngredients([...ingredients, { product_id: 0, quantity: 0, quantity_unit: 'g' }])
  }

  const removeIngredient = (index: number) => {
    setIngredients(ingredients.filter((_, i) => i !== index))
  }

  const updateIngredient = (index: number, field: keyof IngredientInput, value: any) => {
    const updated = [...ingredients]
    updated[index] = { ...updated[index], [field]: value }
    setIngredients(updated)
  }

  const calculateTotalCost = () => {
    let totalCents = 0
    ingredients.forEach(ing => {
      const product = products.find(p => p.id === ing.product_id)
      if (product && product.current_price && ing.quantity > 0) {
        let costCents = 0
        
        console.log('Calculating cost for:', {
          product: product.name,
          price_type: product.price_type,
          package_size: product.package_size,
          quantity: ing.quantity,
          quantity_unit: ing.quantity_unit,
          current_price_cents: product.current_price
        })
        
        // Handle different price types
        // NOTE: product.current_price is in CENTS!
        if (product.price_type === 'per_kg') {
          // Price is per kg, convert quantity to kg
          const qtyInKg = ing.quantity_unit === 'g' ? ing.quantity / 1000 : ing.quantity
          costCents = qtyInKg * product.current_price
          console.log('  -> per_kg calculation:', qtyInKg, 'kg × ', product.current_price, 'cents =', costCents, 'cents')
        } 
        else if (product.price_type === 'per_100g') {
          // Price is per 100g
          const qtyIn100g = ing.quantity_unit === 'g' ? ing.quantity / 100 : ing.quantity * 10
          costCents = qtyIn100g * product.current_price
          console.log('  -> per_100g calculation:', qtyIn100g, '× 100g ×', product.current_price, 'cents =', costCents, 'cents')
        }
        else if (product.price_type === 'per_liter') {
          // Price is per liter
          const qtyInLiters = ing.quantity_unit === 'ml' ? ing.quantity / 1000 : ing.quantity
          costCents = qtyInLiters * product.current_price
          console.log('  -> per_liter calculation:', qtyInLiters, 'l ×', product.current_price, 'cents =', costCents, 'cents')
        }
        else if (product.price_type === 'per_package' && product.package_size) {
          // Price is per package, calculate proportional
          // Convert quantity to match package unit
          let qtyConverted = ing.quantity
          
          if (product.package_unit === 'kg' && ing.quantity_unit === 'g') {
            qtyConverted = ing.quantity / 1000  // g -> kg
          } else if (product.package_unit === 'g' && ing.quantity_unit === 'kg') {
            qtyConverted = ing.quantity * 1000  // kg -> g
          } else if (product.package_unit === 'l' && ing.quantity_unit === 'ml') {
            qtyConverted = ing.quantity / 1000  // ml -> l
          } else if (product.package_unit === 'ml' && ing.quantity_unit === 'l') {
            qtyConverted = ing.quantity * 1000  // l -> ml
          }
          
          costCents = (qtyConverted / product.package_size) * product.current_price
          console.log('  -> per_package calculation:', ing.quantity, ing.quantity_unit, '=', qtyConverted, product.package_unit, '/', product.package_size, '×', product.current_price, 'cents =', costCents, 'cents')
        }
        else {
          // Fallback: use full product price
          costCents = product.current_price
          console.log('  -> fallback: using full price', costCents, 'cents')
        }
        
        totalCents += costCents
      }
    })
    console.log('Total cost (cents):', totalCents)
    return totalCents  // Return in cents for formatPrice()
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!mealForm.name || ingredients.length === 0) {
      setToast({ message: '⚠️ Bitte Namen und mindestens eine Zutat eingeben!', type: 'error' })
      return
    }

    // Validate ingredients
    for (const ing of ingredients) {
      if (!ing.product_id || ing.quantity <= 0) {
        setToast({ message: '⚠️ Bitte alle Zutaten vollständig ausfüllen!', type: 'error' })
        return
      }
    }

    const mealData = {
      name: mealForm.name,
      meal_type: mealForm.meal_type,
      preparation: mealForm.preparation || undefined,
      ingredients: ingredients,
    }

    if (editingMealId) {
      // Update existing meal
      updateMealMutation.mutate({ id: editingMealId, data: mealData })
    } else {
      // Create new meal
      createMealMutation.mutate(mealData)
    }
  }

  const loadMealForEdit = (meal: any) => {
    setEditingMealId(meal.id)
    setMealForm({
      name: meal.name,
      meal_type: meal.meal_type,
      preparation: meal.preparation || '',
    })
    setIngredients(
      meal.ingredients.map((ing: any) => ({
        product_id: ing.product_id,
        quantity: ing.quantity,
        quantity_unit: ing.quantity_unit,
      }))
    )
    setShowForm(true)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const formatPrice = (cents: number) => {
    return `${(cents / 100).toFixed(2)} €`
  }

  const getMealTypeLabel = (type: string) => {
    return MEAL_TYPES.find(t => t.value === type)?.label || type
  }

  const getMealTypeEmoji = (type: string) => {
    return MEAL_TYPES.find(t => t.value === type)?.emoji || '🍽️'
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-[#282828] rounded-lg shadow-xl max-w-6xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="p-6 border-b border-neutral-800 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-neutral-100">🍳 Mahlzeiten</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-neutral-700 rounded-full transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-6">
          {!showForm ? (
            // Meals List View
            <div className="space-y-4">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-neutral-100">Meine Mahlzeiten ({meals.length})</h3>
                <button
                  onClick={() => {
                    resetForm()
                    setShowForm(true)
                  }}
                  className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-medium transition-colors"
                >
                  + Neue Mahlzeit
                </button>
              </div>

              {meals.length === 0 ? (
                <div className="text-center py-12 text-neutral-400">
                  <p className="text-lg">Keine Mahlzeiten vorhanden</p>
                  <p className="text-sm mt-2">Erstelle deine erste Mahlzeit mit Zutaten und Zubereitung!</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {meals.map((meal) => (
                    <div
                      key={meal.id}
                      className="bg-[#1f1f1f] border border-neutral-800 rounded-lg p-5 hover:border-red-500 transition-colors"
                    >
                      {/* Header with Emoji and Title */}
                      <div className="flex items-center gap-3 mb-3">
                        <span className="text-3xl">{getMealTypeEmoji(meal.meal_type)}</span>
                        <div className="flex-1">
                          <h4 className="font-semibold text-neutral-100 text-lg mb-0.5">{meal.name}</h4>
                          <p className="text-xs text-neutral-400">{getMealTypeLabel(meal.meal_type)}</p>
                        </div>
                      </div>

                      {/* Action Buttons */}
                      <div className="flex gap-2 mb-4">
                        <button
                          onClick={() => loadMealForEdit(meal)}
                          className="flex-1 px-3 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors font-medium"
                        >
                          ✏️ Bearbeiten
                        </button>
                        <button
                          onClick={() => setDeleteConfirm({ id: meal.id, name: meal.name })}
                          className="flex-1 px-3 py-2 text-sm bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors font-medium"
                        >
                          🗑️ Löschen
                        </button>
                      </div>

                      <div className="space-y-2 mb-3">
                        <p className="text-xs font-semibold text-neutral-500 uppercase">Zutaten ({meal.ingredients.length})</p>
                        <div className="space-y-1">
                          {meal.ingredients.slice(0, 3).map((ing) => (
                            <div key={ing.id} className="text-sm text-neutral-300 flex items-center justify-between">
                              <span>• {ing.product.name}</span>
                              <span className="text-neutral-500">{ing.quantity}{ing.quantity_unit}</span>
                            </div>
                          ))}
                          {meal.ingredients.length > 3 && (
                            <p className="text-xs text-neutral-500">+ {meal.ingredients.length - 3} weitere</p>
                          )}
                        </div>
                      </div>

                      <div className="pt-3 border-t border-neutral-800 flex items-center justify-between">
                        <span className="text-sm font-medium text-neutral-400">Gesamtkosten:</span>
                        <span className="text-lg font-bold text-red-500">{formatPrice(meal.total_cost_cents)}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            // Meal Form View
            <div className="max-w-3xl mx-auto">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-neutral-100">
                  {editingMealId ? '✏️ Mahlzeit bearbeiten' : '🆕 Neue Mahlzeit erstellen'}
                </h3>
                <button
                  onClick={() => {
                    resetForm()
                    setShowForm(false)
                  }}
                  className="px-3 py-1 text-sm bg-neutral-700 text-neutral-300 rounded hover:bg-neutral-600 transition-colors"
                >
                  Abbrechen
                </button>
              </div>

              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Basic Info */}
                <div className="bg-[#1f1f1f] p-4 rounded-lg space-y-4">
                  <h4 className="font-semibold text-neutral-100">Grundinformationen</h4>
                  
                  <div>
                    <label className="block text-sm font-medium text-neutral-300 mb-1">Name der Mahlzeit</label>
                    <input
                      type="text"
                      placeholder="z.B. Spaghetti Bolognese"
                      value={mealForm.name}
                      onChange={(e) => setMealForm({ ...mealForm, name: e.target.value })}
                      className="w-full px-3 py-2 bg-neutral-800 border border-neutral-700 text-neutral-100 placeholder-neutral-500 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-neutral-300 mb-1">Mahlzeittyp</label>
                    <div className="flex gap-2">
                      {MEAL_TYPES.map((type) => (
                        <button
                          key={type.value}
                          type="button"
                          onClick={() => setMealForm({ ...mealForm, meal_type: type.value })}
                          className={`flex-1 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                            mealForm.meal_type === type.value
                              ? 'bg-red-600 text-white'
                              : 'bg-neutral-700 text-neutral-300 hover:bg-neutral-600'
                          }`}
                        >
                          {type.emoji} {type.label}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Ingredients */}
                <div className="bg-[#1f1f1f] p-4 rounded-lg space-y-4">
                  <div className="flex items-center justify-between">
                    <h4 className="font-semibold text-neutral-100">Zutaten</h4>
                    <button
                      type="button"
                      onClick={addIngredient}
                      className="px-3 py-1 text-sm bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
                    >
                      + Zutat hinzufügen
                    </button>
                  </div>

                  {ingredients.length === 0 ? (
                    <p className="text-sm text-neutral-400 text-center py-4">Noch keine Zutaten hinzugefügt</p>
                  ) : (
                    <div className="space-y-3">
                      {ingredients.map((ing, index) => (
                        <div key={index} className="flex gap-2 items-start">
                          <div className="flex-1">
                            <select
                              value={ing.product_id}
                              onChange={(e) => updateIngredient(index, 'product_id', Number(e.target.value))}
                              className="w-full px-3 py-2 bg-neutral-800 border border-neutral-700 text-neutral-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                              required
                            >
                              <option value={0}>Produkt wählen...</option>
                              {products.map((product) => {
                                const sizeText = product.package_size 
                                  ? product.package_size >= 1000 
                                    ? `${(product.package_size / 1000).toFixed(1)}kg`
                                    : `${product.package_size}${product.package_unit || 'g'}`
                                  : ''
                                return (
                                  <option key={product.id} value={product.id}>
                                    {product.name} {sizeText && `(${sizeText})`}
                                  </option>
                                )
                              })}
                            </select>
                          </div>
                          <div className="flex gap-2">
                            <input
                              type="number"
                              placeholder="Menge"
                              value={ing.quantity || ''}
                              onChange={(e) => updateIngredient(index, 'quantity', Number(e.target.value))}
                              className="w-24 px-3 py-2 bg-neutral-800 border border-neutral-700 text-neutral-100 placeholder-neutral-500 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                              min="0.01"
                              step="0.01"
                              required
                            />
                            <select
                              value={ing.quantity_unit}
                              onChange={(e) => updateIngredient(index, 'quantity_unit', e.target.value)}
                              className="w-20 px-2 py-2 bg-neutral-800 border border-neutral-700 text-neutral-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
                            >
                              <option value="g">g</option>
                              <option value="kg">kg</option>
                              <option value="stück">St.</option>
                              <option value="l">l</option>
                              <option value="ml">ml</option>
                            </select>
                          </div>
                          <button
                            type="button"
                            onClick={() => removeIngredient(index)}
                            className="p-2 text-red-400 hover:bg-red-900 hover:bg-opacity-20 rounded transition-colors"
                            title="Entfernen"
                          >
                            🗑️
                          </button>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Cost Preview */}
                  {ingredients.length > 0 && (
                    <div className="pt-3 border-t border-neutral-800 flex items-center justify-between">
                      <span className="text-sm font-medium text-neutral-400">Geschätzte Kosten:</span>
                      <span className="text-xl font-bold text-red-500">{formatPrice(calculateTotalCost())}</span>
                    </div>
                  )}
                </div>

                {/* Preparation */}
                <div className="bg-[#1f1f1f] p-4 rounded-lg space-y-4">
                  <h4 className="font-semibold text-neutral-100">Zubereitung (optional)</h4>
                  <textarea
                    placeholder="Beschreibe die Zubereitungsschritte..."
                    value={mealForm.preparation}
                    onChange={(e) => setMealForm({ ...mealForm, preparation: e.target.value })}
                    className="w-full px-3 py-2 bg-neutral-800 border border-neutral-700 text-neutral-100 placeholder-neutral-500 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 min-h-[120px]"
                    rows={5}
                  />
                </div>

                {/* Submit */}
                <div className="flex items-center justify-end gap-3">
                  <button
                    type="button"
                    onClick={() => {
                      resetForm()
                      setShowForm(false)
                    }}
                    className="px-4 py-2 bg-neutral-700 text-neutral-200 rounded-lg hover:bg-neutral-600 font-medium transition-colors"
                  >
                    Abbrechen
                  </button>
                  <button
                    type="submit"
                    disabled={createMealMutation.isPending || updateMealMutation.isPending}
                    className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium transition-colors"
                  >
                    {editingMealId 
                      ? (updateMealMutation.isPending ? 'Aktualisiere...' : 'Aktualisieren')
                      : (createMealMutation.isPending ? 'Erstelle...' : 'Mahlzeit erstellen')
                    }
                  </button>
                </div>
              </form>
            </div>
          )}
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <ConfirmModal
          title="Mahlzeit löschen?"
          message={`Möchtest du "${deleteConfirm.name}" wirklich löschen? Diese Aktion kann nicht rückgängig gemacht werden.`}
          confirmText="Löschen"
          cancelText="Abbrechen"
          type="danger"
          onConfirm={() => deleteMealMutation.mutate(deleteConfirm.id)}
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
