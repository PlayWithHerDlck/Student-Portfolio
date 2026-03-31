using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Refacoring
{
    public class UserWithOrdersDto
    {
        //Для примера !
        public int UserId;
        public string Name;
        public List<OrderDto> Orders;
    }
    public class OrderDto
    {
        //Для примера !
        public int OrderId { get; set; }
        public decimal Total { get; set; }

        //реализация класса
    }

    internal class Step2
    {
        string _connectionString;//Для примера!
        public List<UserWithOrdersDto> GetUsersWithOrdersOptimized()
        {
            using (var connection = new SqlConnection(_connectionString))
            {
                connection.Open();
                //1 Один запрос , получаем всех пользователей и их заказы через Join
                const string sql = @"SELECT
                u.Id AS UserID,
                u,Name AS UserName,
                o.Id AS OrderID,
                o.Total AS  OrderTotal
                FROM Users u LEFT JOIN Orders o ON u.Id=o.UserId order by u.ID,o.Id";
                var usersMap = new Dictionary<int, UserWithOrdersDto>();
                using (var cmd = new SqlCommand(sql, connection))
                using (var reader = cmd.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        var userId = reader.GetInt32(reader.GetOrdinal("UserId"));
                        var userName = reader.GetString(reader.GetOrdinal("Username"));
                        //Получаем или создаем пользователя в словаре
                        if (!usersMap.TryGetValue(userId, out var user))
                        {
                            user = new UserWithOrdersDto
                            {
                                UserId = userId,
                                Name = userName,
                                Orders = new List<OrderDto>()
                            };
                            usersMap[userId] = user;
                        }
                        if (!reader.IsDBNull(reader.GetOrdinal("Orderid")))
                        {
                            user.Orders.Add(new OrderDto
                            {
                                OrderId = reader.GetInt32(reader.GetOrdinal("UserId")),
                                Total = reader.GetDecimal(reader.GetOrdinal("OrderTotal"))
                            });
                        }
                    }
                }
            }
        }
    }
}