import asyncio

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import (
    db_helper,
    User,
    Profile,
    Post,
    Order,
    Product,
    OrderProductAssociation,
)


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)  # Find user
    # result: Result = await session.execute(stmt)
    # user: User | None = result.scalar_one_or_none()
    user: User | None = await session.scalar(stmt)  # Short version
    print("found user", username, user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name)
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession):
    stmt = (
        select(User).options(joinedload(User.profile)).order_by(User.id)
    )  # joined load get all data
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.first_name)


async def create_posts(
    session: AsyncSession, user_id: int, *posts_titles: str
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts(session: AsyncSession):
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    stmt = (
        select(User)
        .options(
            # joinedload(User.posts),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    # result: Result = await session.execute(stmt)
    # users = result.unique().scalars()
    users = await session.scalars(stmt)
    # for user in users.unique():
    # users = result.scalars()
    for user in users:
        print("**" * 10)
        print(user)
        for post in user.posts:
            print("-", post)


async def get_users_with_posts_and_profiles(session: AsyncSession):
    stmt = (
        select(User)
        .options(
            joinedload(User.profile),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    users = await session.scalars(stmt)

    for user in users:
        print("**" * 10)
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print("-", post)


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)

    for post in posts:
        print("post", post)
        print("author", post.user)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)  # For filtration
        .options(
            joinedload(Profile.user).selectinload(User.posts),  # Multiply loads
        )
        .where(User.username == "John")  # For filtration
        .order_by(Profile.id)
    )

    profiles = await session.scalars(stmt)

    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def create_order(session: AsyncSession, promocode: str | None = None) -> Order:
    order = Order(promocode=promocode)

    session.add(order)
    await session.commit()

    return order


async def create_product(
    session: AsyncSession, name: str, description: str, price: int
) -> Product:
    product = Product(name=name, description=description, price=price)

    session.add(product)
    await session.commit()

    return product


async def create_products_with_orders(session: AsyncSession):
    order_one = await create_order(session)
    order_promo = await create_order(session, promocode="promo")

    mouse = await create_product(
        session,
        "Mouse",
        "Great gaming mouse",
        price=123,
    )
    keyboard = await create_product(
        session,
        "Keyboard",
        "Great gaming keyboard",
        price=149,
    )
    display = await create_product(
        session,
        "Display",
        "Office display",
        price=299,
    )

    order_one = await session.scalar(
        select(Order)
        .where(Order.id == order_one.id)
        .options(selectinload(Order.products)),
    )
    order_promo = await session.scalar(
        select(Order)
        .where(Order.id == order_promo.id)
        .options(selectinload(Order.products)),
    )

    # Using append(), because we are using lists
    order_one.products.append(mouse)
    order_one.products.append(keyboard)
    # order_promo.products.append(keyboard)
    # order_promo.products.append(display)

    order_promo.products = [keyboard, display]  # Or we can rewrite

    await session.commit()


async def get_orders_with_products(
    session: AsyncSession,
) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products),
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)

    return list(orders)


async def demo_get_orders_with_products_through_secondary(session: AsyncSession):
    orders = await get_orders_with_products(session)
    for order in orders:
        print(order.id, order.promocode, order.created_at, "products:")
        for product in order.products:
            print("-", product.id, product.name, product.price)


async def get_orders_with_products_with_assoc(session: AsyncSession) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAssociation.product
            ),  # We are loading product details and products
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)

    return list(orders)


async def demo_get_orders_with_products_with_assoc(session: AsyncSession):
    orders = await get_orders_with_products_with_assoc(session)

    for order in orders:
        print(order.id, order.promocode, order.created_at, "products:")
        for order_product_details in order.products_details:
            print(
                "-",
                order_product_details.product.id,
                order_product_details.product.name,
                order_product_details.product.price,
                "qty:",
                order_product_details.count,
            )


async def create_gift_product_for_existing_orders(session: AsyncSession):
    orders = await get_orders_with_products_with_assoc(session)
    gift_product = await create_product(
        session,
        name="Gift",
        description="Gift for you",
        price=0,
    )
    for order in orders:
        order.products_details.append(
            OrderProductAssociation(
                count=1,
                unit_price=0,
                product=gift_product,
            )
        )

    await session.commit()


# One-to-many and one-to-one relations def
async def main_relations():
    async with (
        db_helper.session_factory() as session
    ):  # Open session from main.py. db_helper saved a lot of time
        await create_user(session=session, username="John")
        await create_user(session=session, username="Alice")
        await create_user(session=session, username="Sam")
        user_sam = await get_user_by_username(session=session, username="Sam")
        user_john = await get_user_by_username(session=session, username="John")
        # user_bob = await get_user_by_username(session=session, username="Bob")
        await create_user_profile(
            session=session,
            user_id=user_john.id,
            first_name="John",
        )
        await create_user_profile(
            session=session,
            user_id=user_sam.id,
            first_name="Sam",
            last_name="White",
        )
        await show_users_with_profiles(session=session)
        await create_posts(
            session,
            user_john.id,
            "SQLA 2.0",
            "SQLA Joins",
        )
        await create_posts(
            session,
            user_sam.id,
            "FastAPI intro",
            "FastAPI Advanced",
            "FastAPI more",
        )
        await get_users_with_posts(session=session)
        await get_posts_with_authors(session=session)
        await get_users_with_posts_and_profiles(session=session)
        await get_profiles_with_users_and_users_with_posts(session=session)


# Many-to-many relations def
async def demo_m2m(session: AsyncSession):
    # await create_orders_and_products(session)     # Uncomment this if you want
    # await demo_get_orders_with_products_through_secondary(session)
    await demo_get_orders_with_products_with_assoc(session)
    # await create_gift_product_for_existing_orders(session)


async def main():
    async with db_helper.session_factory() as session:
        # await main_relations(session)     # Uncomment to call main_relations def
        await demo_m2m(session)


if __name__ == "__main__":
    asyncio.run(main())
