# Use cases de Subscription -- TODO live coding.
# Replicar el patron de application/use_cases/movie/.
#
# Archivos esperados:
#   contratar_subscription.py   -- valida que el plan exista y este activo;
#                                  calcula expires_at = now + plan.duration_days.
#   listar_subscriptions.py
#   obtener_subscription.py
#   renovar_subscription.py     -- extiende expires_at por otro periodo.
#   cancelar_subscription.py    -- marca is_active=False (no borra historial).
