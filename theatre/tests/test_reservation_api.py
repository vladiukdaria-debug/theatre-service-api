from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from theatre.models import (
    Performance,
    Play,
    TheatreHall,
)


class ReservationApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="testpass123",
        )

        self.other_user = get_user_model().objects.create_user(
            username="other",
            password="testpass123",
        )

        self.play = Play.objects.create(
            title="Hamlet",
            description="Test play",
        )

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

        self.client.force_authenticate(
            user=self.user,
        )

    def test_create_reservation_with_tickets(self):
        payload = {
            "tickets": [
                {
                    "row": 3,
                    "seat": 5,
                    "performance": self.performance.id,
                },
                {
                    "row": 3,
                    "seat": 6,
                    "performance": self.performance.id,
                },
            ]
        }

        response = self.client.post(
            "/api/theatre/reservations/",
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            self.user.reservations.count(),
            1,
        )

        reservation = self.user.reservations.first()

        self.assertEqual(
            reservation.tickets.count(),
            2,
        )

    def test_user_can_see_only_own_reservations(self):
        own_reservation = self.user.reservations.create()

        self.other_user.reservations.create()

        response = self.client.get(
            "/api/theatre/reservations/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["id"],
            own_reservation.id,
        )

    def test_cannot_book_invalid_row(self):
        payload = {
            "tickets": [
                {
                    "row": 50,
                    "seat": 5,
                    "performance": self.performance.id,
                }
            ]
        }

        response = self.client.post(
            "/api/theatre/reservations/",
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_cannot_book_same_seat_twice(self):
        payload = {
            "tickets": [
                {
                    "row": 3,
                    "seat": 5,
                    "performance": self.performance.id,
                }
            ]
        }

        first_response = self.client.post(
            "/api/theatre/reservations/",
            payload,
            format="json",
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_201_CREATED,
        )

        second_response = self.client.post(
            "/api/theatre/reservations/",
            payload,
            format="json",
        )

        self.assertEqual(
            second_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
