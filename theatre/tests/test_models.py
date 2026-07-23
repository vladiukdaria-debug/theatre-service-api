from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from theatre.models import (
    Genre,
    Performance,
    Play,
    Reservation,
    TheatreHall,
    Ticket,
)


class TicketModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )

        self.genre = Genre.objects.create(
            name="Drama",
        )

        self.play = Play.objects.create(
            title="Hamlet",
            description="Test play",
        )

        self.play.genres.add(self.genre)

        self.hall = TheatreHall.objects.create(
            name="Main Hall",
            rows=10,
            seats_in_row=20,
        )

        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time="2026-08-10T19:00:00Z",
        )

        self.reservation = Reservation.objects.create(
            user=self.user,
        )

    def test_ticket_created_successfully(self):
        ticket = Ticket.objects.create(
            row=3,
            seat=5,
            performance=self.performance,
            reservation=self.reservation,
        )

        self.assertEqual(ticket.row, 3)
        self.assertEqual(ticket.seat, 5)

    def test_ticket_row_cannot_exceed_hall_rows(self):
        ticket = Ticket(
            row=11,
            seat=5,
            performance=self.performance,
            reservation=self.reservation,
        )

        with self.assertRaises(ValidationError):
            ticket.full_clean()

    def test_ticket_seat_cannot_exceed_hall_seats(self):
        ticket = Ticket(
            row=3,
            seat=21,
            performance=self.performance,
            reservation=self.reservation,
        )

        with self.assertRaises(ValidationError):
            ticket.full_clean()
