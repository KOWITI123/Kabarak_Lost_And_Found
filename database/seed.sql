-- Insert sample items
INSERT INTO items (item_name, description, location_found, status, date_reported) VALUES
('Blue Backpack', 'Nike backpack with books', 'Library', 'Found', CURRENT_TIMESTAMP - INTERVAL '2 days'),
('iPhone 13', 'Black case, cracked screen', 'Cafeteria', 'Claim Pending', CURRENT_TIMESTAMP - INTERVAL '1 day'),
('Water Bottle', 'Metal flask, green', 'Sports Complex', 'Returned', CURRENT_TIMESTAMP - INTERVAL '3 days'),
('Calculus Textbook', 'Thomas Calculus 14th Ed', 'Library', 'Found', CURRENT_TIMESTAMP - INTERVAL '5 hours'),
('Car Keys', 'Toyota keys with keychain', 'Parking Lot A', 'Found', CURRENT_TIMESTAMP - INTERVAL '1 hour');

-- Insert sample claims
INSERT INTO claims (item_id, claimant_name, student_reg_no, status) VALUES
(2, 'John Doe', 'REG-2023-001', 'Pending Approval'),
(3, 'Jane Smith', 'REG-2023-002', 'Approved');
