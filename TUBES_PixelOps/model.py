from abc import ABC, abstractmethod

class User:
    def __init__(self, nama):
        self.__nama = nama

    def get_nama(self):
        return self.__nama

    def set_nama(self, nama):
        self.__nama = nama

class Admin(User):
    def __init__(self, nama):
        super().__init__(nama)

class Designer(User):
    def __init__(self, nama, spesialis):
        super().__init__(nama)
        self.__spesialis = spesialis

    def get_spesialis(self):
        return self.__spesialis

    def set_spesialis(self, spesialis):
        self.__spesialis = spesialis

class Client:
    def __init__(self, nama, perusahaan, email, telepon):
        self.__nama = nama
        self.__perusahaan = perusahaan
        self.__email = email
        self.__telepon = telepon

    def get_data(self):
        return (
            self.__nama,
            self.__perusahaan,
            self.__email,
            self.__telepon
        )

class Project(ABC):

    def __init__(self, nama_project, deadline, budget):
        self._nama_project = nama_project
        self._deadline = deadline
        self._budget = budget

    @abstractmethod
    def jenis_project(self):
        pass

    def tampilkan_info(self):
        return {
            "Nama Project": self._nama_project,
            "Jenis": self.jenis_project(),
            "Deadline": self._deadline,
            "Budget": self._budget
        }

class LogoProject(Project):

    def jenis_project(self):
        return "Logo Design"


class BrandingProject(Project):

    def jenis_project(self):
        return "Branding"


class PosterProject(Project):

    def jenis_project(self):
        return "Poster Design"


class SocialMediaProject(Project):

    def jenis_project(self):
        return "Social Media Design"


class UIUXProject(Project):

    def jenis_project(self):
        return "UI/UX Design"


class MotionProject(Project):

    def jenis_project(self):
        return "Motion Graphic"

class Revision:

    def __init__(self, revisi_ke, catatan, tanggal):
        self.revisi_ke = revisi_ke
        self.catatan = catatan
        self.tanggal = tanggal

    def tampilkan_revisi(self):
        return {
            "Revisi": self.revisi_ke,
            "Catatan": self.catatan,
            "Tanggal": self.tanggal
        }

class Payment:

    def __init__(self, total, dp):
        self.__total = total
        self.__dp = dp

    def hitung_sisa(self):
        return self.__total - self.__dp

    def status(self):
        if self.hitung_sisa() == 0:
            return "Lunas"
        elif self.__dp > 0:
            return "DP"
        else:
            return "Belum Bayar"