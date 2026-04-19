from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from .models import Image

class ImageTestUtils:
    @staticmethod
    def create_image(**kwargs):
        defaults = {
            'image_name': 'test',
            'image_url': 'images/test.jpg',
            'is_active': True
        }
        defaults.update(kwargs)
        return Image.objects.create(**defaults)

    def get_response(self, template: str, *args):
        if args:
             return self.client.get(reverse(template, args=[*args]))
        return self.client.get(reverse(template))



class ImageIndexViewTest(TestCase, ImageTestUtils):

    def get_index_response(self):
        return self.get_response('images:index')

    def test_index_returns_200(self):
        response = self.get_index_response()

        self.assertEqual(response.status_code, 200)

    def test_index_uses_correct_template(self):
        response = self.get_index_response()

        self.assertTemplateUsed(response, 'images/index.html')

    def test_index_context_contains_image(self):
        Image.objects.create(image_name='test', image_url='images/test.jpg')
        Image.objects.create(image_name='test2', image_url='images/test2.jpg')

        response = self.get_index_response()

        image_list = response.context['image_list']
        self.assertEqual(len(image_list), 2)

    def test_index_context_contains_correct_images(self):
        image1 = Image.objects.create(image_name='test', image_url='images/test.jpg')
        image2 = Image.objects.create(image_name='test2', image_url='images/test2.jpg')

        response = self.get_index_response()

        image_list = response.context['image_list']
        self.assertIn(image1, image_list)
        self.assertIn(image2, image_list)

    def test_index_with_no_images(self):
        response = self.get_index_response()

        image_list = response.context['image_list']

        self.assertEqual(len(image_list), 0)

    def test_index_view(self):
        image = Image.objects.create(image_name='test', image_url='images/test.jpg')

        response = self.get_index_response()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/index.html')

        image_list = response.context['image_list']
        self.assertEqual(image_list.count(), 1)
        self.assertIn(image, image_list)

class ImageDetailViewTest(TestCase, ImageTestUtils):

        def get_detail_response(self, image_id):
            return self.get_response('images:detail', image_id)

        def test_detail_returns_200(self):
            image = self.create_image()

            response = self.get_detail_response(image.id)

            self.assertEqual(response.status_code, 200)

        def test_detail_returns_404(self):
            response = self.get_detail_response(1)

            self.assertEqual(response.status_code, 404)

        def test_detail_view_using_correct_template(self):
            image = self.create_image()
            response = self.get_detail_response(image.id)

            self.assertTemplateUsed(response, 'images/detail.html')

class ImageDeleteViewTest(TestCase, ImageTestUtils):

    def get_delete_response(self, image_id):
         return self.get_response('images:delete', image_id)

    def test_correct_deleting_image(self):
        image1 = self.create_image(image_name='image1', image_url='images/image1.jpeg')
        image2 = self.create_image(image_name='image2', image_url='images/image2.jpeg')
        image_list_before_deleting = Image.objects.all()

        self.get_delete_response(image1.id)


        image_list_after_deleting = Image.objects.all()
        self.assertNotEqual(image_list_before_deleting, image_list_after_deleting)
        self.assertNotIn(image1, image_list_after_deleting)
        self.assertIn(image2, image_list_after_deleting)

    def test_incorrect_deleting_image_with_code_404(self):
        image = self.create_image()
        self.get_delete_response(image.id)

        response = self.get_delete_response(image.id)

        self.assertEqual(response.status_code, 404)

    def test_correct_redirect_template(self):
        image = self.create_image()

        response = self.get_delete_response(image.id)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('images:index'))

class ImageUploadViewTest(TestCase, ImageTestUtils):
    def get_upload_response(self):
        return self.get_response('images:upload')

    def post_upload_response(self, data):
        return self.client.post(reverse('images:upload'), data)

    def test_upload_get_returns_code_200(self):
        response = self.get_upload_response()

        self.assertEqual(response.status_code, 200)

    def test_upload_get_uses_correct_template(self):
        response = self.get_upload_response()

        self.assertTemplateUsed(response, 'images/upload.html')

    def test_upload_post_valid_data_creates_image_and_redirects(self):
        uploaded_file = SimpleUploadedFile(
            "test.gif",
            (
                b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00"
                b"\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21"
                b"\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00"
                b"\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44"
                b"\x01\x00\x3b"
            ),
            content_type="image/gif",
        )

        response = self.post_upload_response(
            {
                "image_name": "test",
                "image_url": uploaded_file,
            }
        )

        self.assertEqual(Image.objects.count(), 1)
        self.assertRedirects(response, reverse("images:index"))

        image = Image.objects.first()
        self.assertEqual(image.image_name, "test")

    def test_upload_post_invalid_file_does_not_create_object(self):
        invalid_file = SimpleUploadedFile(
            "test.txt",
            b"not an image",
            content_type="text/plain",
        )

        response = self.client.post(
            reverse("images:upload"),
            {
                "image_name": "bad_file",
                "image_url": invalid_file,
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "images/upload.html")
        self.assertEqual(Image.objects.count(), 0)
        self.assertTrue(response.context["form"].errors)

