"""Add conversation and message tables for AI chatbot

Revision ID: 001_chatbot_tables
Revises:
Create Date: 2026-02-06

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_chatbot_tables'
down_revision = None  # Update this to your last migration if exists
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create conversations and messages tables with indexes."""

    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes on conversations
    op.create_index(
        'ix_conversations_user_id',
        'conversations',
        ['user_id'],
        unique=False
    )
    op.create_index(
        'ix_conversations_created_at',
        'conversations',
        ['created_at'],
        unique=False
    )

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('conversation_id', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint("role IN ('user', 'assistant')", name='check_message_role')
    )

    # Create indexes on messages
    op.create_index(
        'ix_messages_conversation_id',
        'messages',
        ['conversation_id'],
        unique=False
    )
    op.create_index(
        'ix_messages_created_at',
        'messages',
        ['created_at'],
        unique=False
    )


def downgrade() -> None:
    """Drop conversations and messages tables."""
    op.drop_index('ix_messages_created_at', table_name='messages')
    op.drop_index('ix_messages_conversation_id', table_name='messages')
    op.drop_table('messages')

    op.drop_index('ix_conversations_created_at', table_name='conversations')
    op.drop_index('ix_conversations_user_id', table_name='conversations')
    op.drop_table('conversations')
