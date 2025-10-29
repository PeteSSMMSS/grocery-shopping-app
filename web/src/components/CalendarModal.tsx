import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../lib/api'
import ConfirmModal from './ConfirmModal'
import Toast from './Toast'

interface CalendarModalProps {
  onClose: () => void
}

interface ShoppingEvent {
  id: number
  name: string
  event_date: string
  total_price_cents: number
  items: Array<{ product_id: number; product_name: string; qty: number; price_cents: number }>
  created_at: string
}

export default function CalendarModal({ onClose }: CalendarModalProps) {
  const queryClient = useQueryClient()
  const today = new Date()
  const [currentMonth, setCurrentMonth] = useState(today.getMonth())
  const [currentYear, setCurrentYear] = useState(today.getFullYear())
  const [selectedDate, setSelectedDate] = useState<string | null>(null)
  const [deleteConfirm, setDeleteConfirm] = useState<number | null>(null)
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null)

  // Fetch shopping events for current month
  const { data: events = [] } = useQuery({
    queryKey: ['shopping-events', currentYear, currentMonth + 1],
    queryFn: () => api.shoppingEvents.getByMonth(currentYear, currentMonth + 1),
  })

  // Delete event
  const deleteMutation = useMutation({
    mutationFn: (id: number) => api.shoppingEvents.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['shopping-events'] })
      setSelectedDate(null)
      setDeleteConfirm(null)
      setToast({ message: 'Einkauf erfolgreich gelöscht!', type: 'success' })
    },
    onError: (error: any) => {
      setDeleteConfirm(null)
      setToast({ message: 'Fehler beim Löschen: ' + error.message, type: 'error' })
    },
  })

  // Calendar helpers
  const monthNames = [
    'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
    'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'
  ]

  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate()
  const firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay()
  const adjustedFirstDay = firstDayOfMonth === 0 ? 6 : firstDayOfMonth - 1 // Monday = 0

  // Navigate months
  const goToPreviousMonth = () => {
    if (currentMonth === 0) {
      setCurrentMonth(11)
      setCurrentYear(currentYear - 1)
    } else {
      setCurrentMonth(currentMonth - 1)
    }
    setSelectedDate(null)
  }

  const goToNextMonth = () => {
    if (currentMonth === 11) {
      setCurrentMonth(0)
      setCurrentYear(currentYear + 1)
    } else {
      setCurrentMonth(currentMonth + 1)
    }
    setSelectedDate(null)
  }

  // Get events for a specific day
  const getEventsForDay = (day: number) => {
    const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
    return events.filter((event: ShoppingEvent) => event.event_date === dateStr)
  }

  // Format price
  const formatPrice = (cents: number) => {
    return `${(cents / 100).toFixed(2)} €`
  }

  // Get events for selected date
  // Get events for selected date
  const selectedEvents = selectedDate ? events.filter((event: ShoppingEvent) => event.event_date === selectedDate) : []

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-[#282828] rounded-lg max-w-4xl w-full max-h-[90vh] overflow-auto">
        {/* Header */}
        <div className="sticky top-0 bg-[#282828] border-b border-neutral-700 p-4 flex items-center justify-between z-10">
          <h2 className="text-xl font-bold text-neutral-100">📅 Einkaufskalender</h2>
          <button
            onClick={onClose}
            className="text-neutral-400 hover:text-neutral-200 text-2xl leading-none"
          >
            ×
          </button>
        </div>

        {!selectedDate ? (
          <>
            {/* Month Navigation */}
            <div className="p-4 flex items-center justify-between border-b border-neutral-700">
              <button
                onClick={goToPreviousMonth}
                className="px-4 py-2 bg-neutral-700 text-neutral-200 rounded-lg hover:bg-neutral-600 transition"
              >
                ← Zurück
              </button>
              <h3 className="text-lg font-semibold text-neutral-100">
                {monthNames[currentMonth]} {currentYear}
              </h3>
              <button
                onClick={goToNextMonth}
                className="px-4 py-2 bg-neutral-700 text-neutral-200 rounded-lg hover:bg-neutral-600 transition"
              >
                Weiter →
              </button>
            </div>

            {/* Calendar Grid */}
            <div className="p-4">
              {/* Weekday Headers */}
              <div className="grid grid-cols-7 gap-2 mb-2">
                {['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'].map((day) => (
                  <div key={day} className="text-center text-sm font-medium text-neutral-400 py-2">
                    {day}
                  </div>
                ))}
              </div>

              {/* Calendar Days */}
              <div className="grid grid-cols-7 gap-2">
                {/* Empty cells for days before month starts */}
                {Array.from({ length: adjustedFirstDay }).map((_, i) => (
                  <div key={`empty-${i}`} className="aspect-square" />
                ))}

                {/* Days of the month */}
                {Array.from({ length: daysInMonth }).map((_, i) => {
                  const day = i + 1
                  const dayEvents = getEventsForDay(day)
                  const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
                  const isToday = 
                    day === today.getDate() &&
                    currentMonth === today.getMonth() &&
                    currentYear === today.getFullYear()
                  
                  const totalPrice = dayEvents.reduce((sum: number, event: ShoppingEvent) => sum + event.total_price_cents, 0)

                  return (
                    <div
                      key={day}
                      onClick={() => dayEvents.length > 0 && setSelectedDate(dateStr)}
                      className={`
                        aspect-square p-2 rounded-lg border transition-all
                        ${isToday ? 'border-red-500 bg-red-900/20' : 'border-neutral-700'}
                        ${dayEvents.length > 0 ? 'bg-emerald-900/30 hover:bg-emerald-900/50 cursor-pointer' : 'bg-neutral-800/50'}
                      `}
                      title={dayEvents.length > 0 ? dayEvents.map((e: ShoppingEvent) => 
                        `${e.name}: ${e.items.map((i) => i.product_name).join(', ')}`
                      ).join('\n') : ''}
                    >
                      <div className="h-full flex flex-col">
                        <div className={`text-sm font-medium ${isToday ? 'text-red-400' : 'text-neutral-300'}`}>
                          {day}
                        </div>
                        {dayEvents.length > 0 && (
                          <div className="mt-auto">
                            <div className="text-xs font-semibold text-emerald-400">
                              {formatPrice(totalPrice)}
                            </div>
                            <div className="text-xs text-neutral-500">
                              {dayEvents.length}× Einkauf
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </>
        ) : (
          /* Detail View for Selected Date */
          <div className="p-6">
            <button
              onClick={() => setSelectedDate(null)}
              className="mb-4 px-4 py-2 bg-neutral-700 text-neutral-200 rounded-lg hover:bg-neutral-600 transition"
            >
              ← Zurück zum Kalender
            </button>

            <h3 className="text-lg font-semibold text-neutral-100 mb-4">
              Einkäufe am {new Date(selectedDate).toLocaleDateString('de-DE', { day: '2-digit', month: 'long', year: 'numeric' })}
            </h3>

            <div className="space-y-4">
              {selectedEvents.map((event: ShoppingEvent) => (
                <div key={event.id} className="bg-neutral-800 border border-neutral-700 rounded-lg p-4">
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <h4 className="font-semibold text-neutral-100 text-lg">{event.name}</h4>
                      <p className="text-sm text-neutral-400">
                        {new Date(event.created_at).toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit' })} Uhr
                      </p>
                    </div>
                    <div className="text-right">
                      <div className="text-xl font-bold text-emerald-400">
                        {formatPrice(event.total_price_cents)}
                      </div>
                      <button
                        onClick={() => setDeleteConfirm(event.id)}
                        className="mt-2 px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700 transition"
                      >
                        🗑️ Löschen
                      </button>
                    </div>
                  </div>

                  {/* Products List */}
                  <div className="border-t border-neutral-700 pt-3">
                    <p className="text-xs font-medium text-neutral-400 mb-2">Produkte:</p>
                    <div className="space-y-1">
                      {event.items.map((item, idx) => (
                        <div key={idx} className="flex justify-between text-sm">
                          <span className="text-neutral-300">
                            {item.qty}× {item.product_name}
                          </span>
                          <span className="text-neutral-400">
                            {formatPrice(item.price_cents * item.qty)}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Delete Confirmation Modal */}
      {deleteConfirm && (
        <ConfirmModal
          title="Einkauf löschen?"
          message="Möchtest du diesen Einkauf wirklich löschen? Diese Aktion kann nicht rückgängig gemacht werden."
          confirmText="Löschen"
          cancelText="Abbrechen"
          type="danger"
          onConfirm={() => deleteMutation.mutate(deleteConfirm)}
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
