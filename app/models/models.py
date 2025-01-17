from sqlalchemy import (
    Column, Integer, String, Boolean, Float, ForeignKey, DateTime, Text, func
)
from sqlalchemy.orm import relationship
from app.infra.database.database import Base

# Tabela status
class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

# Tabela users
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    status_id = Column(Integer, ForeignKey('status.id'), default='user')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    status = relationship('Status', back_populates='users')

Status.users = relationship('User', back_populates='status')

# Tabela country
class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    iso_code = Column(String(3), unique=True, nullable=False)

# Tabela market
class Market(Base):
    __tablename__ = 'market'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    country_id = Column(Integer, ForeignKey('country.id'))

    country = relationship('Country', back_populates='markets')

Country.markets = relationship('Market', back_populates='country')

# Tabela assets
class Asset(Base):
    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(50))
    market_id = Column(Integer, ForeignKey('market.id'))

    market = relationship('Market', back_populates='assets')

Market.assets = relationship('Asset', back_populates='market')

# Tabela asset_price_history
class AssetPriceHistory(Base):
    __tablename__ = 'asset_price_history'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    dividends = Column(Float)
    stock_splits = Column(Float)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False)

    asset = relationship('Asset', back_populates='price_history')

Asset.price_history = relationship('AssetPriceHistory', back_populates='asset')

# Tabela transaction_types
class TransactionType(Base):
    __tablename__ = 'transaction_types'

    id = Column(Integer, primary_key=True)
    type_name = Column(String(50), nullable=False)

# Tabela portfolio
class Portfolio(Base):
    __tablename__ = 'portfolio'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship('User', back_populates='portfolios')

User.portfolios = relationship('Portfolio', back_populates='user')

# Tabela  asset_transactions
class AssetTransaction(Base):
    __tablename__ = 'asset_transactions'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    unit_value = Column(Float, nullable=False)
    purchase_value = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    
    portfolio_id = Column(Integer, ForeignKey('portfolio.id'), nullable=False)
    transaction_type_id = Column(Integer, ForeignKey('transaction_types.id'))
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    portfolio = relationship('Portfolio', back_populates='portfolio_assets')
    transaction_type = relationship('TransactionType', back_populates='transactions')
    asset = relationship('Asset', back_populates='user_transactions')

Portfolio.portfolio_assets = relationship('AssetTransaction', back_populates='portfolio')
TransactionType.transactions = relationship('AssetTransaction', back_populates='transaction_type')
Asset.user_transactions = relationship('AssetTransaction', back_populates='asset')





