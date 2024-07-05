from database.models import async_session
from database.models import Admin, Report, Bus
from sqlalchemy import select, update, asc
import datetime as dt

async def is_admin(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(Admin).where(Admin.tg_id ==  tg_id))
        return user

async def ins_report (tg_id,
                      state_number, 
                      appearance, 
                      cl_interior, 
                      cl_seat, 
                      cl_handles, 
                      seat_integrity, 
                      checklist, 
                      portfolio,
                      seat_belts,
                      drivers_appearance,
                      behaviour,
                      briefing,
                      temperature,
                      comment,
                      ranked):
    async with async_session() as session:
        async with session.begin():
            date = dt.date.today()
            new_report = Report(tg_id = tg_id,
                    state_number = state_number,
                    appearance = appearance, 
                    cl_interior = cl_interior,
                    cl_seat = cl_seat,
                    cl_handles = cl_handles,
                    seat_integrity = seat_integrity,
                    checklist = checklist,
                    portfolio = portfolio,
                    seat_belts = seat_belts,
                    drivers_appearance = drivers_appearance,
                    behaviour = behaviour,
                    briefing = briefing,
                    temperature = temperature,
                    comment = comment,
                    ranked = ranked,
                    date=date,
                    status=0,
                    comment_moder='Оценка еще не рассмотрена.')
            session.add(new_report)
        await session.commit()

async def get_bus_by_state_number (state_number):
    async with async_session() as session:
        result = await session.scalar(select(Bus).where(Bus.state_number ==  state_number))
        return result

async def check_reps(tg_id):
    async with async_session() as session:
        stmt = select(Report).where(Report.tg_id == tg_id)
        result = await session.execute(stmt)
        reps = result.scalars().all()
        return reps

async def get_report_by_id (id):
    async with async_session() as session:
        stmt = select(Report).where(Report.id == id)
        result = await session.execute(stmt)
        reps = result.scalars().all()
        return reps

async def check_moder_reps(status):
    async with async_session() as session:
        stmt = select(Report).where(Report.status == status).order_by(asc(Report.date))
        result = await session.execute(stmt)
        reps = result.scalars().all()
        return reps

async def update_comment_moder(report_id, comment_moder):
    async with async_session() as session:
        async with session.begin():
            stmt = (
                update(Report)
                .where(Report.id == report_id)
                .values(comment_moder=comment_moder, status = 1)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(stmt)
            await session.commit()

async def is_moder(lvl):
    async with async_session() as session:
        stmt = select(Admin).where(Admin.level ==  lvl)
        result = await session.execute(stmt)
        moders = result.scalars().all()
        return moders
    
async def ins_moder (tg_id):
    async with async_session() as session:
        async with session.begin():
            new_moder = Admin(tg_id = tg_id, level = 1)
            session.add(new_moder)
        await session.commit()

async def delete_moder (id):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(Admin).where(Admin.id == id))
            admin = result.scalar_one_or_none()
            await session.delete(admin)
        await session.commit()

async def admin_by_id(id):
    async with async_session() as session:
        user = await session.scalar(select(Admin).where(Admin.id == id))
        return user