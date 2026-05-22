# ============================================================================
# SCHEMAS Pydantic: Subscription  -- TODO live coding
# ============================================================================
# Plantilla: ver application/schemas/movie_schema.py
#
# Campos: group_id, plan_id, expires_at (datetime).
# Sugerencia: en el use case ContratarSubscription, expires_at se calcula
# como datetime.now() + timedelta(days=plan.duration_days). El cliente
# NO lo envia.
# ============================================================================

# TODO: definir SubscriptionCreate (solo group_id + plan_id),
#       SubscriptionRead (incluye expires_at + started_at + is_active),
#       SubscriptionUpdate (renovar / cancelar).
